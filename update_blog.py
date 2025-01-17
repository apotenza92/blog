import os
import re
import shutil
import time
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Configuration
CONFIG = {
    # Repository settings
    "repo": {
        "owner": "apotenza92",
        "name": "blog",
    },
    # Folder structure
    "folders": {
        "posts": "posts",
        "images": "images",
        "static": "static",
        "content": "content",
        "public": "public",
    },
    # File paths
    "files": {"config": "hugo.toml"},
    # Workflow settings
    "workflow": {"check_delay": 10, "max_checks": 30},  # seconds  # 5 minutes maximum
}


def find_onedrive_root():
    """Find OneDrive root directory across different OS configurations"""
    possible_paths = [
        os.path.expanduser("~/OneDrive"),  # Windows/Mac default
        os.path.expanduser("~/OneDrive - Personal"),  # Business account variant
        "/Users/Shared/OneDrive",  # Alternative Mac location
        os.path.expanduser(
            "~/Library/CloudStorage/OneDrive-Personal"
        ),  # New Mac location
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    raise FileNotFoundError("Could not find OneDrive folder")


def find_obsidian_vault(start_path, vault_name="Notes"):
    """Find Obsidian vault by looking for .obsidian folder"""
    # First try direct path
    direct_path = os.path.join(start_path, vault_name)
    if os.path.exists(os.path.join(direct_path, ".obsidian")):
        return direct_path

    # Search recursively up to 2 levels deep
    for root, dirs, _ in os.walk(start_path):
        if ".obsidian" in dirs:
            return root
        # Don't go too deep
        if root.count(os.sep) - start_path.count(os.sep) >= 2:
            dirs.clear()

    raise FileNotFoundError(f"Could not find Obsidian vault '{vault_name}'")


def get_latest_workflow_run():
    try:
        # Get workflows started in the last 5 minutes
        current_time = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(
            [
                "gh",
                "api",
                f"/repos/{CONFIG['repo']['owner']}/{CONFIG['repo']['name']}/actions/runs?created=>2023-01-01&per_page=5",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        runs = json.loads(result.stdout).get("workflow_runs", [])

        # Find the most recent "in_progress" or "queued" run
        for run in runs:
            if run["status"] in ["in_progress", "queued"]:
                return run
        return runs[0] if runs else None
    except subprocess.CalledProcessError as e:
        print(f"Error getting workflow runs: {e}")
        return None


def wait_for_workflow():
    delay = CONFIG["workflow"]["check_delay"]
    max_checks = CONFIG["workflow"]["max_checks"]

    print(f"\nWaiting {delay} seconds for workflow to start...")
    time.sleep(delay)

    print("Checking workflow status...")
    attempts = 0

    while attempts < max_checks:
        run = get_latest_workflow_run()
        if not run:
            print("No workflow run found")
            break

        status = run["status"]
        conclusion = run["conclusion"]
        run_id = run["id"]

        if status == "completed":
            if conclusion == "success":
                print("\n✅ Workflow completed successfully!")
            else:
                print(f"\n❌ Workflow failed with conclusion: {conclusion}")
                repo = CONFIG["repo"]
                print(
                    f"Check: https://github.com/{repo['owner']}/{repo['name']}/actions/runs/{run_id}"
                )
            break

        print(f"Status: {status}... (checking again in {delay} seconds)")
        time.sleep(delay)
        attempts += 1

    if attempts >= max_checks:
        print("\n⚠️ Timed out waiting for workflow to complete")


def setup_paths():
    """Initialize and validate all required paths"""
    try:
        onedrive_root = find_onedrive_root()
        ob_root = find_obsidian_vault(onedrive_root)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Falling back to default path...")
        ob_root = os.path.expanduser("~/OneDrive/Notes")

    # Setup paths
    paths = {
        "obsidian": {
            "root": ob_root,
            "posts": os.path.join(ob_root, CONFIG["folders"]["posts"]),
        },
        "hugo": {
            "root": os.path.dirname(os.path.abspath(__file__)),
        },
    }

    # Add hugo subpaths
    paths["hugo"]["posts"] = os.path.join(
        paths["hugo"]["root"], CONFIG["folders"]["content"], CONFIG["folders"]["posts"]
    )
    paths["hugo"]["images"] = os.path.join(
        paths["hugo"]["root"], CONFIG["folders"]["static"], CONFIG["folders"]["images"]
    )

    # Create necessary directories
    os.makedirs(paths["hugo"]["posts"], exist_ok=True)
    os.makedirs(paths["hugo"]["images"], exist_ok=True)

    return paths


def sync_posts(paths):
    """Sync posts from Obsidian to Hugo"""
    try:
        subprocess.run(
            [
                "rsync",
                "-av",
                "--delete",
                f"{paths['obsidian']['posts']}/",
                f"{paths['hugo']['posts']}/",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error during rsync: {e}")
        if not os.path.exists(paths["obsidian"]["posts"]):
            print(f"Source directory {paths['obsidian']['posts']} does not exist!")
            return False
    return True


def process_images(paths):
    """Process and copy images from posts"""
    wiki_pattern = r"!\[\[([^]]*\.(?:png|jpe?g))\]\]"

    for filename in os.listdir(paths["hugo"]["posts"]):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(paths["hugo"]["posts"], filename)
        with open(filepath, "r") as file:
            content = file.read()

        wiki_images = re.findall(wiki_pattern, content, re.IGNORECASE)
        if not wiki_images:
            continue

        print(f"\nProcessing {filename}")
        print(f"Found {len(wiki_images)} images:")

        for idx, rel_path in enumerate(wiki_images, 1):
            source = os.path.join(paths["obsidian"]["root"], rel_path)
            image_filename = os.path.basename(rel_path)

            # Convert wikilink to markdown
            repo = CONFIG["repo"]
            new_link = (
                f"![](/{repo['name']}/images/{image_filename.replace(' ', '%20')})"
            )
            content = content.replace(f"![[{rel_path}]]", new_link)

            if os.path.exists(source):
                shutil.copy(source, paths["hugo"]["images"])
                print(f"  ✓ [{idx}] {image_filename}")
            else:
                print(
                    f"  ✗ [{idx}] {image_filename} (not found in {os.path.dirname(rel_path)})"
                )

        with open(filepath, "w") as file:
            file.write(content)


def update_blog(paths):
    """Build and deploy blog updates"""
    # Clean public folder
    subprocess.run(
        ["rm", "-rf", CONFIG["folders"]["public"]],
        cwd=paths["hugo"]["root"],
        check=True,
    )

    # Build and push
    subprocess.run(["hugo"], check=True)
    subprocess.run(["git", "add", "."], cwd=paths["hugo"]["root"], check=True)
    subprocess.run(
        ["git", "commit", "-m", "Updated blog"], cwd=paths["hugo"]["root"], check=True
    )
    subprocess.run(["git", "push"], cwd=paths["hugo"]["root"], check=True)


def update_hugo_config(paths):
    """Update Hugo configuration file with correct baseURL"""
    config_path = os.path.join(paths["hugo"]["root"], CONFIG["files"]["config"])
    repo = CONFIG["repo"]
    new_base_url = f'baseURL = \'https://{repo["owner"]}.github.io/{repo["name"]}/\''

    if not os.path.exists(config_path):
        print(f"Warning: Hugo config file not found at {config_path}")
        return

    with open(config_path, "r") as file:
        lines = file.readlines()

    # Update baseURL line
    for i, line in enumerate(lines):
        if line.strip().startswith("baseURL"):
            lines[i] = f"{new_base_url}\n"
            break

    with open(config_path, "w") as file:
        file.writelines(lines)

    print(f"Updated Hugo config baseURL to {new_base_url}")


def main():
    # Setup
    paths = setup_paths()

    # Update Hugo config
    update_hugo_config(paths)

    # Sync and process
    if not sync_posts(paths):
        return

    process_images(paths)
    print("\nFinished Processing Images!")

    # Update and deploy
    update_blog(paths)
    print("\nBlog Updated and Changes Committed!")

    # Check deployment
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
        wait_for_workflow()
    except FileNotFoundError:
        print(
            "\nWarning: GitHub CLI (gh) not found. Please install it to track workflow status."
        )
        print("Install with: brew install gh")

    # Open blog
    repo = CONFIG["repo"]
    blog_url = f"https://{repo['owner']}.github.io/{repo['name']}/"
    subprocess.run(["open", blog_url], check=True)


if __name__ == "__main__":
    main()
