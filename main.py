import os
from threading import Thread
import eel

from tkinter import Tk, messagebox

from app.utils.main import reset_db, InsertionStatus
from app.utils.filemanager import list_files, open_dir
from app.utils.filemanager import get_files_by_account
from app.utils.filemanager import create_config_path
from app.utils.filemanager import set_initial_struct_dirs
from app.utils.filemanager import get_month_directories
from app.utils.filemanager import select_dir, select_file
from app.utils.filemanager import remove_directory

from app.data.main import get_classified_files
from app.data.main import get_month_inserted_items
from app.data.main import move_classified_files
from app.data.main import get_modelized_items

from app.autom.routine import insert_item

from app.config.globals import screen_size
from app.config.paths import syspath
from app.config.settings import set_chromedriver_path
from app.config.settings import get_chromedriver_path
from app.config.settings import get_chromedriver_settings
from app.config.settings import get_chromedriver_version
from app.config.settings import set_browserwindow_show
from app.config.settings import get_browserwindow_show
from app.config.credentials import Credential
from app.config.user import User

from app.execlogs.logs import *
from app.execlogs.notifications import *

STATUS: InsertionStatus = None


@eel.expose
def is_user_set() -> bool:
    user_credential = Credential()
    user_data = user_credential.get_user_credentials()

    return not len(user_data) == 0


@eel.expose
def remove_current_user() -> bool:
    return reset_db()


@eel.expose
def set_driver_path(driver_path: str) -> bool:
    return set_chromedriver_path(driver_path)


@eel.expose
def get_driver_path() -> str:
    return get_chromedriver_path()


@eel.expose
def get_driver_version() -> str:
    return get_chromedriver_version()


@eel.expose
def get_driver_settings() -> dict:
    return get_chromedriver_settings()


@eel.expose
def set_browser_window_show(show: bool) -> bool:
    return set_browserwindow_show(show)


@eel.expose
def get_browser_window_show() -> bool:
    return get_browserwindow_show()


@eel.expose
def get_month_directory_list() -> list:
    return get_month_directories()


@eel.expose
def get_sys_path() -> str:
    return syspath

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

    return user_data[0] if len(user_data) > 0 else ""


@eel.expose
def set_user_credential(username: str, passwd: str) -> bool:
    user = User(username, passwd)
    user_credential = Credential()

    return user_credential.set_user_credential(user.get_user(), user.get_pass())


@eel.expose
def get_folder_path() -> str:
    return select_dir()


@eel.expose
def select_file_path() -> str:
    return select_file()


@eel.expose
def get_screen_size() -> list:
    return screen_size


@eel.expose
def create_work_directory(work_month: str) -> bool:
    work_month_path: str = os.path.join(syspath, work_month.replace("/", "-"))                   
    return set_initial_struct_dirs(work_month_path)


@eel.expose
def get_work_month_path(month: str) -> str:
    work_month_path: str = os.path.join(syspath, month.replace("/", "-"))                   
    return work_month_path


@eel.expose
def insert_new_item(month:str, work_month_path: str, 
    items_list: list, no_window) -> None:
    global STATUS
    STATUS = InsertionStatus()

    Thread(
        target = insert_item, 
        args = (month.replace("-", "/"), 
        work_month_path, items_list, no_window, STATUS)
    ).start()

    logs: list = get_execlogs()
    for log in logs: print(log[1])
    clear_logs()


@eel.expose
def remove_notification(id: int) -> bool:
    return delete_notification(id)


@eel.expose
def clear_all_notifications() -> bool:
    return clear_notifications()


@eel.expose
def get_notification_list() -> list:
    return get_notifications()
    

@ eel.expose
def alert(title: str, msg:str) -> None:
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.iconbitmap()
    messagebox.showinfo(title, msg)
    root.destroy()


@eel.expose
def month_has_inserted_debts(month: str) -> bool:        
    return len(get_month_inserted_items(month)) > 0
    

@eel.expose 
def get_files_from_folder() -> bool:
    path: str = select_dir()

    success: bool = False
    if path is not None:
        classified_files = get_classified_files(path)

        for item in classified_files:
            success = move_classified_files(path, item)

            if not success:
                document_already_inserted(item)
        
    return success


@eel.expose
def get_current_status() -> dict:
    global STATUS
    return STATUS.get_status()


@eel.expose
def clear_status() -> None:
    global STATUS
    STATUS = None


@eel.expose
def get_data(work_month: str, all: bool = False) -> dict:

    if work_month is None: return
    work_month_path: str = os.path.join(syspath, work_month.replace("/", "-"))
    
    if ".pdf" in work_month_path or ".png" in work_month_path or ".jpg" in work_month_path:
        return

    files: list = list_files(work_month_path)
    
    if len(files) > 0:
        items_1000, items_1010 = get_files_by_account(files)

        modelized_items_1000: list[dict] = get_modelized_items(items_1000)
        modelized_items_1010: list[dict] = get_modelized_items(items_1010)

        if all:
            all_items: list[dict] = modelized_items_1000 + modelized_items_1010
            return {"all": all_items}

        return {"1000": modelized_items_1000, "1010": modelized_items_1010}

    return {"1000": [], "1010": []}


def main() -> None:
    create_config_path()
    eel.init("src")
    eel.start("index.html", port=8091, size=(int(screen_size[0]), int(screen_size[1])), position=(230, 50))


if __name__ == "__main__":
    main()
    