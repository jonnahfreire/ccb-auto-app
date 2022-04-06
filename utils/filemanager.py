import os

from config.globals import WIN, struct_dirs, debt_code_list
from execlogs.logs import *
from cli.colors import *

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


def get_files_path(work_path: str) -> list:
    files_path = []

    for dir in struct_dirs:
        for sub_dir in os.listdir(os.path.join(work_path, dir[0])):
            for file_name in os.listdir(os.path.join(work_path, dir[0], sub_dir)):
                if file_name:
                    full_path = os.path.join(work_path, dir[0], 
                        os.path.join(work_path, dir[0], sub_dir), file_name)
                    files_path.append(full_path)
    return files_path


def list_files(base_path: str) -> list:
    base_accounts = []

    if os.path.exists(base_path):
        dirs = os.listdir(base_path)
        base_accounts = [a for a in dirs]

    account_files = []
    for account in base_accounts:
        accounts = os.listdir(os.path.join(base_path, account))

        for acc in accounts:
            files_by_account = os.listdir(os.path.join(base_path, account, acc))
            files_by_account = [file for file in files_by_account if file != "Lancados"]
            if files_by_account:
                account_files.append({account: {acc.split("-")[0].strip(): files_by_account}})

    return account_files


def get_files_by_account(files: list) -> tuple[list]:
    debts_1000, debts_1010 = [], []

    for debts in files:
        for key in debts.keys():
            if key == "1000":
                debts_1000.append(debts[key])

            elif key == "1010":
                debts_1010.append(debts[key])
        
    return debts_1000, debts_1010


def move_file_to(path: str, filename: str) -> bool:
    if os.path.exists(path):
        if not WIN: 
            os.system(f"mv '{filename}' {path}")
            return True
        else: pass # Windows Implementation
    return False


def copy_file_to(path: str, filename: str) -> bool:
    if os.path.exists(path):
        if not WIN: 
            os.system(f"cp '{filename}' '{path}'")
            return True
        else: pass # Windows Implementation
    return False


def rename_file_to(filename: str, newname: str) -> bool:
    if os.path.isfile(filename):
        if not WIN: 
            os.system(f"mv '{filename}' '{newname}'")
            return True
        else: pass # Windows Implementation
    return False


def path_scape_space(path: str) -> str:
    pass