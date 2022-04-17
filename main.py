import os
from threading import Thread
import eel

from tkinter import Tk, messagebox

from utils.main import reset_db
from utils.filemanager import list_files, open_dir
from utils.filemanager import get_files_by_account
from utils.filemanager import create_config_path
from utils.filemanager import set_initial_struct_dirs
from utils.filemanager import get_month_directories
from utils.filemanager import select_dir
from utils.filemanager import remove_directory

from data.main import get_classified_files 
from data.main import move_classified_files_to_sist_path
from data.main import get_modelized_debts

from autom.routine import insert_debt, status

from config.globals import sist_path, screen_size
from config.credentials import Credential
from config.user import User

from execlogs.logs import *


@eel.expose
def is_user_set() -> bool:
    create_config_path()
    user_credential = Credential()
    user_data = user_credential.get_user_credentials()

    if len(user_data) == 0:
        return False
    return True


@eel.expose
def remove_current_user() -> bool:
    return reset_db()


@eel.expose
def get_month_directory_list() -> list:
    return get_month_directories()


@eel.expose
def get_sys_path() -> str:
    return sist_path

@eel.expose
def open_directory(path: str) -> None:
    return open_dir(path)


@eel.expose
def remove_month_directory(dirname) -> bool:
    return remove_directory(dirname)


@eel.expose
def get_username() -> str:
    user_credential = Credential()
    user_data = user_credential.get_user_credentials()

    if len(user_data) > 0:
        return user_data[0]
    
    return ""


@eel.expose
def set_user_credential(username: str, passwd: str) -> bool:
    user = User(username, passwd)
    user_credential = Credential()

    if user_credential.set_user_credential(user.get_user(), user.get_pass()):
        return True
    
    return False


@eel.expose
def get_folder_path():
    return select_dir()


@eel.expose
def get_screen_size():
    return screen_size


@eel.expose
def create_work_directory(work_month: str) -> bool:
    work_month_path: str = os.path.join(sist_path, work_month.replace("/", "-"))                   
    return set_initial_struct_dirs(work_month_path)


@eel.expose
def get_work_month_path(month: str) -> str:
    work_month_path: str = os.path.join(sist_path, month.replace("/", "-"))                   
    return work_month_path


@eel.expose
def insert_new_debt(month:str, 
        work_month_path: str, 
        debt_list: list[dict], 
        window: bool = False) -> None:
        
    Thread(target=insert_debt,
        args=(
            month.replace("-", "/"),
            work_month_path,
            debt_list,
            window
        )
    ).start()

    logs: list = get_execlogs()
    for log in logs: print(log[1])


@ eel.expose
def alert(title: str, msg:str) -> None:
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.iconbitmap()
    messagebox.showinfo(title, msg)
    root.destroy()


@eel.expose 
def get_files_from_folder() -> bool:
    path: str = select_dir()

    success: bool = False
    if path is not None:
        classified_files = get_classified_files(path)

        for i in classified_files:
            success = move_classified_files_to_sist_path(path, i)
        
    return success


@eel.expose
def get_current_status() -> dict:
    return status


@eel.expose
def get_data(work_month, all=False):

    if work_month is None: pass
    work_month_path: str = os.path.join(sist_path, work_month.replace("/", "-"))

    files: list = list_files(work_month_path)

    if len(files) > 0:
        debts_1000, debts_1010 = get_files_by_account(files)

        modelized_debts_1000: list[dict] = get_modelized_debts(debts_1000)
        modelized_debts_1010: list[dict] = get_modelized_debts(debts_1010)

        if all:
            all_debts: list[dict] = modelized_debts_1000 + modelized_debts_1010
            return all_debts

        return {"1000": modelized_debts_1000, "1010": modelized_debts_1010}

    return {"1000": [], "1010": []}


def main() -> None:
    eel.init("./UI/src")
    eel.start("index.html", port=8090, size=(int(screen_size[0]), int(screen_size[1])), position=(230, 50))


if __name__ == "__main__":
    main()
    