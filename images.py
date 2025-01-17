import os
import re
import shutil

# Paths
posts_dir = "/Users/alexpotenza/Documents/alexblog/content/posts"
notes_dir = "/Users/alexpotenza/OneDrive/Notes"  # Root of notes
static_images_dir = "/Users/alexpotenza/Documents/alexblog/static/images"

# Pattern that matches any wikilink with relative path from Notes folder
wiki_pattern = r"!\[\[([^]]*\.(?:png|jpe?g))\]\]"

# Process each markdown file
for filename in os.listdir(posts_dir):
    if not filename.endswith(".md"):
        continue

    filepath = os.path.join(posts_dir, filename)
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
        source = os.path.join(notes_dir, rel_path)
        image_filename = os.path.basename(rel_path)

        # Convert wikilink to markdown
        new_link = f"![Image Description](/images/{image_filename.replace(' ', '%20')})"
        content = content.replace(f"![[{rel_path}]]", new_link)

        # Copy image if it exists
        if os.path.exists(source):
            shutil.copy(source, static_images_dir)
            print(f"  ✓ [{idx}] {image_filename}")
        else:
            print(
                f"  ✗ [{idx}] {image_filename} (not found in {os.path.dirname(rel_path)})"
            )

    # Save changes
    with open(filepath, "w") as file:
        file.write(content)

print("\nDone!")
