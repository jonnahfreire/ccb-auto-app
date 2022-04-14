import os
import eel

from tkinter import Tk, messagebox

from utils.filemanager import list_files
from utils.filemanager import get_files_by_account
from utils.filemanager import create_config_path
from utils.filemanager import set_initial_struct_dirs
from utils.filemanager import get_month_directories
from utils.filemanager import select_dir

from data.main import get_modelized_debts
from config.globals import sist_path, screen_size

from config.credentials import Credential
from config.user import User


@eel.expose
def is_user_set() -> bool:
    create_config_path()
    user_credential = Credential()
    user_data = user_credential.get_user_credentials()

    if len(user_data) == 0:
        return False
    return True


@eel.expose
def get_month_directory_list() -> list:
    return get_month_directories()


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


@ eel.expose
def alert(title: str, msg:str) -> None:
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.iconbitmap()
    messagebox.showinfo(title, msg)
    root.destroy()


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


@eel.expose
def main(work_month: str) -> None:
    pass


if __name__ == "__main__":
    eel.init("UI/src")
    eel.start("index.html", port=8090, size=(int(screen_size[0]), int(screen_size[1])), position=(230, 50))

    