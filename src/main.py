import os
import shutil
import re
from textnode import markdown_to_html_node
from htmlnode import LeafNode, ParentNode

def delete_directory_contents(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    print(f"Deleted contents of {directory}")

def copy_directory(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        
        if os.path.isfile(s):
            shutil.copy2(s, d)
            print(f"Copied file: {s} to {d}")
        else:
            copy_directory(s, d)
            print(f"Copied directory: {s} to {d}")

def extract_title(markdown):
    match = re.search(r'^\s*#\s*(.+)$', markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError("No h1 header found in the markdown content")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f:
        markdown_content = f.read()

    with open(template_path, 'r') as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    
    if html_node is None:
        html_content = ""
    elif isinstance(html_node, (LeafNode, ParentNode)):
        html_content = html_node.to_html()
    else:
        raise TypeError(f"Expected LeafNode or ParentNode, got {type(html_node)}")

    # Extract hyperlinks using regular expression
    hyperlinks = re.findall(r'href=[\'"]?([^\'" >]+)', html_content)

    title = extract_title(markdown_content)

    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(full_html)
    print(f"Written HTML content to {dest_path}")

    # Print extracted hyperlinks
    print("Extracted hyperlinks:")
    for link in hyperlinks:
        print(link)

    return hyperlinks

def main():
    public_dir = "public"
    
    # Delete anything in the public directory
    if os.path.exists(public_dir):
        delete_directory_contents(public_dir)
    else:
        os.makedirs(public_dir)
    
    # Copy all static files from static to public
    copy_directory("static", public_dir)
    
    # Generate the index page
    generate_page("content/index.md", "template.html", os.path.join(public_dir, "index.html"))
    
    print("Static site generation complete.")

if __name__ == "__main__":
    main()