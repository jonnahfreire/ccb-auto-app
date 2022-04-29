import os
from tkinter import Tk, filedialog
from app.utils.main import WIN
from app.config.globals import struct_dirs, debt_code_list, sist_path, config
from app.execlogs.logs import *
from app.cli.colors import *


def create_config_path() -> bool:
    config_dir = os.path.join(sist_path, config)
    try:
        if not os.path.exists(sist_path):
            os.mkdir(sist_path)

        if not os.path.exists(config_dir):
            os.mkdir(config_dir)
            return True
            
    except Exception:
        return False


def get_month_directories() -> list:
    if os.path.exists(sist_path):
        return [
            month for month in sorted(os.listdir(sist_path)) 
            if not month.startswith(".")
            and not month == "config"
            and os.path.isdir(os.path.join(sist_path, month))
            and not os.path.isfile(os.path.join(sist_path, month))
        ]

    return []


def set_initial_struct_dirs(work_month_path: str) -> bool:
    try:
        if not os.path.exists(sist_path):
            os.mkdir(sist_path)
        
        if WIN:
            win_config_path = os.path.join(sist_path, config)
            if os.path.exists(win_config_path):
                os.system("attrib +h {}".format(win_config_path))
        
        # Create ccb-autom/03-2022 Ex.
        if not os.path.exists(work_month_path):
            os.makedirs(work_month_path)
        
            for struct in struct_dirs:
                create_struct_dir(work_month_path, struct[1:], struct[0])
            
            return True
            
    except Exception:
        return False


def create_struct_dir(path: str, sub_dirs: list, top_dir: str) -> None:
    try:
        os.makedirs(os.path.join(path, top_dir))
        
        for dir in sub_dirs:
            for index, debt_code in enumerate(debt_code_list):
                if dir == debt_code.split("-")[0].strip():
                    dirname = "-".join(debt_code_list[index].split(" "))
                    os.mkdir(os.path.join(path, top_dir, dirname))
                    
    except FileExistsError as err:
        insert_execlog(f"{red}Error Creating Struct Dirs:\n\t{yellow}{err}{bg}")


def create_dir(path: str, dirname: str) -> bool:
    if os.path.exists(path):
        if os.path.isdir(os.path.join(path, dirname)):
            return False

        try:
            os.mkdir(os.path.join(path, dirname))
            return True
        except FileExistsError as err:
            insert_execlog(f"{red}Error Creating Directory {dirname}:\n\t{yellow}{err}{bg}")
    return False


def get_files_path(work_path: str) -> list[str]:
    files_path: list[str] = []

    for dir in struct_dirs:
        for sub_dir in os.listdir(os.path.join(work_path, dir[0])):
            for file_name in os.listdir(os.path.join(work_path, dir[0], sub_dir)):
                if file_name:
                    full_path:str = os.path.join(work_path, dir[0], 
                        os.path.join(work_path, dir[0], sub_dir), file_name)
                    files_path.append(full_path)
    return files_path


def list_files(base_path: str) -> list[dict]:
    base_accounts:list = []

    if os.path.exists(base_path):
        dirs:list[str] = os.listdir(base_path)
        base_accounts:list[str] = [a for a in dirs]

    account_files:list[dict] = []
    for account in base_accounts:
        accounts:list[str] = os.listdir(os.path.join(base_path, account))

        for acc in accounts:
            files_by_account:list[str] = os.listdir(os.path.join(base_path, account, acc))
            files_by_account:list[str] = [file for file in files_by_account if file != "Lancados"]
            if files_by_account:
                account_files.append({account: {acc.split("-")[0].strip(): files_by_account}})

    return account_files


def get_files_by_account(files: list) -> tuple[list]:
    items_1000, items_1010 = [], []

    for items in files:
        for key in items.keys():
            if key == "1000":
                items_1000.append(items[key])

            elif key == "1010":
                items_1010.append(items[key])
        
    return items_1000, items_1010


def move_file_to(path: str, filename: str) -> bool:
    if os.path.exists(path):
        if not WIN: 
            os.system(f"mv '{filename}' {path}")
            return True
        else: # Windows Implementation
            os.system(f"move '{filename}' {path}")
            return True 
    return False


def remove_directory(dirname: str) -> bool:   
    dirpath: str = os.path.join(sist_path, dirname)

    if os.path.exists(dirpath):
        if not WIN: 
            os.system(f"rm -rf '{dirpath}'")
        else: # Windows Implementation
            os.system(f"RMDIR /S /Q {dirpath}")

        return True 
    return False


def copy_file_to(path: str, filename: str) -> bool:
    """Copy file to the path specified

    @params:
        path (str): path to copy file to
        filename (str): name of file including it's local path
        
    returns:
        bool: True if success, else False"""
    if os.path.exists(path):
        if not WIN: 
            os.system(f"cp '{filename}' '{path}'")
            
        else: # Windows Implementation
            os.system(f"copy /Y \"{filename}\" {path}")
        
        return True
    return False


def rename_file_to(filename: str, newname: str) -> bool:
    if os.path.isfile(filename):
        if not WIN: 
            os.system(f"mv '{filename}' '{newname}'")
            return True
        else: # Windows Implementation
            os.rename(filename, newname)
            return True
    return False


def select_dir() -> str:
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    dirpath = filedialog.askdirectory(title="Selecione o diretório dos arquivos")
    root.destroy()
    return dirpath


def open_dir(dirpath: str) -> None:
    path = os.path.realpath(dirpath)
    if not WIN: os.system(f"xdg-open {path}")
    else: os.startfile(path)


