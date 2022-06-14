import os
from threading import Thread

from tkinter import Tk, messagebox

from app.config.itemsdb import get_all_items
from app.config.itemsdb import get_items1000
from app.config.itemsdb import get_items1010
from app.config.itemsdb import get_extract_items

from app.utils.main import reset_db, InsertionStatus
from app.utils.filemanager import open_dir
from app.utils.filemanager import create_config_path
from app.utils.filemanager import set_initial_struct_dirs
from app.utils.filemanager import get_month_directories
from app.utils.filemanager import select_dir, select_file
from app.utils.filemanager import remove_directory

from app.data.main import get_classified_files
from app.data.main import get_month_inserted_items
from app.data.main import move_classified_files
from app.data.main import set_extract_file_data
from app.data.main import set_fileitems_data

from app.autom.routine import insert_item

from app.config.globals import screen_size
from app.config.paths import syspath
from app.config.settings import set_chromedriver_path
from app.config.settings import get_chromedriver_path
from app.config.settings import get_chromedriver_settings
from app.config.settings import get_chromedriver_version
from app.config.settings import set_browserwindow_show
from app.config.settings import get_browserwindow_show

from app.config.itemsdb import get_item_id
from app.config.itemsdb import remove_item
from app.config.itemsdb import set_inserted_item

from app.config.credentials import Credential
from app.config.user import User

from app.execlogs.logs import *
from app.execlogs.notifications import *

STATUS: InsertionStatus = None



def is_user_set() -> bool:
    user_credential = Credential()
    user_data = user_credential.get_user_credentials()

    return not len(user_data) == 0



def remove_current_user() -> bool:
    return reset_db()



def set_driver_path(driver_path: str) -> bool:
    return set_chromedriver_path(driver_path)



def get_driver_path() -> str:
    return get_chromedriver_path()



def get_driver_version() -> str:
    return get_chromedriver_version()



def get_driver_settings() -> dict:
    return get_chromedriver_settings()



def set_browser_window_show(show: bool) -> bool:
    return set_browserwindow_show(show)



def get_browser_window_show() -> bool:
    return get_browserwindow_show()



def get_month_directory_list() -> list:
    return get_month_directories()




def get_id(table: str, item: dict) -> int:
    return get_item_id(table, item)



def get_sys_path() -> str:
    return syspath


def open_directory(path: str) -> None:
    return open_dir(path)



def remove_month_directory(dirname: str) -> bool:
    return remove_directory(dirname)



def remove_item_document(item: dict) -> bool:
    return remove_item(item)



def set_item_as_sent(item: dict) -> bool:
    return set_inserted_item(item)



def restaure_sent_item(item: dict, inserted: int = 0) -> bool:
    return set_inserted_item(item, inserted)



def get_username() -> str:
    user_credential = Credential()
    user_data = user_credential.get_user_credentials()

    return user_data[0] if len(user_data) > 0 else ""



def set_user_credential(username: str, passwd: str) -> bool:
    user = User(username, passwd)
    user_credential = Credential()

    return user_credential.set_user_credential(user.get_user(), user.get_pass())



def get_folder_path() -> str:
    return select_dir()



def select_file_path() -> str:
    return select_file()



def get_screen_size() -> list:
    return screen_size



def create_work_directory(work_month: str) -> bool:
    work_month_path: str = os.path.join(syspath, work_month.replace("/", "-"))                   
    return set_initial_struct_dirs(work_month_path)



def get_work_month_path(month: str) -> str:
    work_month_path: str = os.path.join(syspath, month.replace("/", "-"))                   
    return work_month_path



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



def remove_notification(id: int) -> bool:
    return delete_notification(id)



def clear_all_notifications() -> bool:
    return clear_notifications()



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



def month_has_inserted_debts(month: str) -> bool:        
    return len(get_month_inserted_items(month)) > 0
    


def set_extract_data(filepath: str) -> bool:
    return set_extract_file_data(filepath)


 
def get_files_from_folder(path: str) -> bool:
    success: bool = False
    if path is not None:
        classified_files = get_classified_files(path)

        for item in classified_files:
            success = move_classified_files(path, item)

            if not success:
                document_already_inserted(item)
        
        set_fileitems_data()
    return success



def get_current_status() -> dict:
    global STATUS
    return STATUS.get_status()



def clear_status() -> None:
    global STATUS
    STATUS = None



def get_data(work_month: str, items1000: bool,
    items1010: bool, extract_items: bool, inserted: int) -> dict:
    
    if work_month is None: return
    if not items1000 and not items1010 and not extract_items:
        return get_all_items(work_month, inserted)
        
    elif items1000 and not items1010 and not extract_items:
        return get_items1000(work_month, inserted)

    elif items1010 and not items1000 and not extract_items:
        return get_items1010(work_month, inserted)

    elif extract_items and not items1000 and not items1010:
        return get_extract_items(work_month, inserted)



def set_files_data() -> bool:
    return set_fileitems_data()
    

def main() -> None:
    create_config_path()
    


if __name__ == "__main__":
    main()
    