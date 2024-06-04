import os
from markdowntohtml import MarkdownToHtml
from pathlib import Path
import re
import shutil

def copy_dir(from_dir):
    """This is a stupid function writen just for fun. Don't use it for real"""
    if not os.path.exists(from_dir):
        raise ValueError("From path does not exist")

    project_root = Path(os.path.abspath(__file__)).parent.parent.absolute()
    print(f'Project root: {project_root}')
    public_dir = os.path.join(project_root, 'public')
    print(f'Will copy to {public_dir}.\nDeleting current {public_dir}')
    shutil.rmtree(public_dir)
    print(f'{public_dir} exists: {os.path.exists(public_dir)}')

    print(f'Creating new {public_dir}')
    os.mkdir(public_dir)
    print(f'{public_dir} exists: {os.path.exists(public_dir)}')

    def copy(from_dir, to_dir):
        in_dir = os.listdir(from_dir)
        print(f'Currently at {from_dir}')
        for link in in_dir:
            cur_path = os.path.join(from_dir, link)
            if os.path.isfile(cur_path):
                print(f'Copying {link} to {to_dir}')
                shutil.copy(cur_path, to_dir)
            else:
                print(f'{cur_path} is a dir')
                to_dir = os.path.join(to_dir, link)
                os.mkdir(to_dir)
                copy(cur_path, to_dir)
        print(f'Finished dir {from_dir}')

    copy(from_dir, public_dir)

def extract_title(markdown):
    title = re.search(r'(?<!#)# ([^\n]+)', markdown)
    if not title:
        raise ValueError("Must contain a header")
    return title.group(1)

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path, 'r') as file:
        raw_markdown = file.read()

    md_parser = MarkdownToHtml()

    converted = md_parser.markdown_to_html(raw_markdown)
    title = extract_title(raw_markdown)

    with open(template_path, 'r') as file:
        template = file.read()

    template = template.replace('{{ Title }}', title).replace('{{ Content }}', converted)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    with open(os.path.join(dest_path, 'index.html'), 'w') as f:
        f.write(template)


def main():
    project_root = Path(os.path.abspath(__file__)).parent.parent.absolute()
    static_path = os.path.join(project_root, 'static')
    copy_dir(static_path)

    generate_page(
        os.path.join(project_root, 'content', 'index.md'),
        os.path.join(project_root, 'template.html'),
        os.path.join(project_root, 'public'),
    )

if __name__ == '__main__':
    main()
