import shutil
import os

from block_markdown import markdown_to_html_node, extract_title

def copy_static_to_public(path="static"):
    if path == "static":
        # delete contents of destination public
        shutil.rmtree("public")

        # make the public directory
        os.mkdir("public")

    # copy everything from static, recursively
    static_contents = os.listdir(path)
    for static_content in static_contents:
        curr_path = os.path.join(path, static_content)
        if os.path.isfile(curr_path):
            shutil.copy(curr_path, curr_path.replace("static", "public", 1))
        else:
            os.mkdir(os.path.join("public", static_content))
            copy_static_to_public(curr_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        contents = f.read()
    with open(template_path) as f:
        template = f.read()
    html_string = markdown_to_html_node(contents).to_html()
    title = extract_title(contents)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    with open(dest_path, "w+") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content="content", template_path="template.html", dest_dir_path="public"):
    contents = os.listdir(dir_path_content)
    for content in contents:
        curr_path = os.path.join(dir_path_content, content)
        if os.path.isfile(curr_path):
            generate_page(curr_path, template_path, os.path.join(dest_dir_path, content).replace(".md", ".html"))
        else:
            os.mkdir(os.path.join(dest_dir_path, content))
            generate_pages_recursive(curr_path, template_path, os.path.join(dest_dir_path, content))

def main():
    copy_static_to_public()
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive()

main()
