from textnode import *
from filework import *
import sys
#print("hello world")

if len(sys.argv) > 1:
    BASEPATH = sys.argv[1]
else:
    BASEPATH = "/"


def main ():
    #testnode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    #print (repr(testnode))
    target_path_cleanup("docs")
    copy_source_to_target("static","docs")
    generate_page_recursively("content", "template.html", "docs")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f: from_content = f.read()
    with open(template_path) as g: template_content = g.read()
    #print (from_content)
    #print (template_content)
    title = extract_title(from_content)
    #print(title)
    #print (template_content.replace("{{ Title }}",title))
    content_nodes = markdown_to_html_node(from_content)
    #print(content_nodes)
    content_html = content_nodes.to_html()
    #print(content_html)
    result = template_content.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    result = result.replace('href="/',f'href="{BASEPATH}')
    result = result.replace('src="/',f'src="{BASEPATH}')
    dir_dest = os.path.dirname(dest_path)
    if not os.path.exists(dir_dest):
        os.makedirs(dir_dest,exist_ok=True)
        #print(f"Dest_path {dir_dest} created")
    with open(dest_path, 'w') as h: print(result, file=h)

def generate_page_recursively(dir_path_content, template_path, dest_dir_path):
    print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}")
    for object in os.listdir(dir_path_content):
        object_with_path = f"{dir_path_content}/{object}"
        target_with_path = f"{dest_dir_path}/{object}"
        if os.path.isfile(object_with_path):
            if object.endswith(".md"):
                target_with_path = target_with_path.replace('.md','.html')
                generate_page(object_with_path, template_path, target_with_path)
                print("Processed source:", object_with_path)
        elif os.path.isdir(object_with_path):
            generate_page_recursively(object_with_path, template_path, target_with_path)

main()

