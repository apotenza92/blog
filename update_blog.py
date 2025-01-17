import os
import re
import shutil
import time
import json
import subprocess
from datetime import datetime, timezone

# Obsidian Paths - removed leading slashes
ob_root = "/Users/alexpotenza/OneDrive/Notes"
ob_posts = os.path.join(ob_root, "posts")

# Hugo paths - removed leading slashes
hugo_root = "/Users/alexpotenza/Documents/alexblog"
hugo_images = os.path.join(hugo_root, "static", "images")
hugo_posts = os.path.join(hugo_root, "content", "posts")

# Create necessary directories if they don't exist
os.makedirs(hugo_posts, exist_ok=True)
os.makedirs(hugo_images, exist_ok=True)

# Sync obsidian posts folder with Hugo posts folder
try:
    subprocess.run(
        ["rsync", "-av", "--delete", f"{ob_posts}/", f"{hugo_posts}/"],
        check=True,
    )
except subprocess.CalledProcessError as e:
    print(f"Error during rsync: {e}")
    print(f"Checking if source directory exists: {ob_posts}")
    if not os.path.exists(ob_posts):
        print(f"Source directory {ob_posts} does not exist!")
        exit(1)

# Pattern that matches any wikilink with relative path from Notes folder
wiki_pattern = r"!\[\[([^]]*\.(?:png|jpe?g))\]\]"

# Process each markdown file
for filename in os.listdir(hugo_posts):
    if not filename.endswith(".md"):
        continue

    filepath = os.path.join(hugo_posts, filename)
    with open(filepath, "r") as file:
        content = file.read()

    # Find all wikilinks
    wiki_images = re.findall(wiki_pattern, content, re.IGNORECASE)

    if not wiki_images:
        continue

    print(f"\nProcessing {filename}")
    print(f"Found {len(wiki_images)} images:")

    # Process each image
    for idx, rel_path in enumerate(wiki_images, 1):
        # Get full path relative to Notes directory
        source = os.path.join(ob_root, rel_path)
        image_filename = os.path.basename(rel_path)

        # Convert wikilink to markdown
        new_link = f"![](/blog/images/{image_filename.replace(' ', '%20')})"
        content = content.replace(f"![[{rel_path}]]", new_link)

        # Copy image if it exists
        if os.path.exists(source):
            shutil.copy(source, hugo_images)
            print(f"  ✓ [{idx}] {image_filename}")
        else:
            print(
                f"  ✗ [{idx}] {image_filename} (not found in {os.path.dirname(rel_path)})"
            )

    # Save changes
    with open(filepath, "w") as file:
        file.write(content)

print("\nFinished Processing Images!")

# Empty out existing public folder
subprocess.run(["rm", "-rf", "public"], cwd=hugo_root, check=True)

# Update blog
subprocess.run(["hugo"], check=True)

print("\nBlog Updated!")

# Commit changes
subprocess.run(["git", "add", "."], cwd=hugo_root, check=True)
subprocess.run(["git", "commit", "-m", "Updated blog"], cwd=hugo_root, check=True)
subprocess.run(["git", "push"], cwd=hugo_root, check=True)

print("\nChanges Committed!")

# Add GitHub API configuration
REPO_OWNER = "apotenza92"
REPO_NAME = "blog"


def get_latest_workflow_run():
    try:
        # Get workflows started in the last 5 minutes
        current_time = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(
            [
                "gh",
                "api",
                f"/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs?created=>2023-01-01&per_page=5",
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
    print("\nWaiting 10 seconds for workflow to start...")
    time.sleep(10)  # Initial delay to let workflow start

    print("Checking workflow status...")
    attempts = 0
    max_attempts = 30  # 5 minutes maximum wait time

    while attempts < max_attempts:
        run = get_latest_workflow_run()
        if not run:
            print("No workflow run found")
            break

        status = run["status"]
        conclusion = run["conclusion"]
        run_id = run["id"]

        print(f"Run ID: {run_id}")
        print(f"Current status: {status}")
        print(f"Conclusion: {conclusion}")

        if status == "completed":
            if conclusion == "success":
                print("\n✅ Workflow completed successfully!")
            else:
                print(f"\n❌ Workflow failed with conclusion: {conclusion}")
                print(
                    f"Check: https://github.com/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}"
                )
            break

        print(f"Status: {status}... (checking again in 10 seconds)")
        time.sleep(10)
        attempts += 1

    if attempts >= max_attempts:
        print("\n⚠️ Timed out waiting for workflow to complete")


# Check workflow status using gh cli
try:
    subprocess.run(["gh", "--version"], check=True, capture_output=True)
    wait_for_workflow()
except FileNotFoundError:
    print(
        "\nWarning: GitHub CLI (gh) not found. Please install it to track workflow status."
    )
    print("Install with: brew install gh")

# Open blog at https://apotenza92.github.io/blog/
subprocess.run(["open", "https://apotenza92.github.io/blog/"], check=True)
