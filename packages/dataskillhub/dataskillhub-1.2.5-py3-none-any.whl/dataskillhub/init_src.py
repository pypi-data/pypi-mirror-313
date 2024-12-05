import shutil
from pathlib import Path


def create_folder(folder_name: str):
    folder_path = Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)


def copy_file(folder_source, folder_target, file_name):
    path = Path(__file__).parent
    copier_path = path.parent / folder_source / file_name
    paste_path = f"{folder_target}/{file_name}"
    shutil.copyfile(copier_path, paste_path)
