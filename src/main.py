import os
from pathlib import Path
import shutil
import sys

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

if __name__ == '__main__':
    copy_dir(sys.argv[1])
