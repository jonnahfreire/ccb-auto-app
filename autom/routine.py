from time import sleep

from autom.main import Selenium
from autom.strings import ccb_siga
from autom.siga import Siga
from autom.msgs import *

from config.credentials import Credential

from utils.main import InsertionStatus
from utils.filemanager import create_dir
from utils.filemanager import get_files_path, move_file_to


SUCCESSFUL_SENT: list = []
FAIL_SENDING   : list = []
EXISTING_FILES : list = []


def set_initial_status(current: dict, status: InsertionStatus) -> None:
    status.set_current(current)
    status.set_finished(False)
    status.set_failed(False)
    status.set_started()


def get_file_path(files_path: str, filename: str) -> str:
    return [
        files_path[files_path.index(fp)]
        for fp in files_path
        if filename in fp
    ][0]


def insert_item(work_month: str, work_month_path:str, 
    data: list, window: bool, status: InsertionStatus) -> None:

    del SUCCESSFUL_SENT[:]
    del FAIL_SENDING   [:]
    del EXISTING_FILES [:]

    if len(data) == 0: return

    user, passwd = Credential().get_user_credentials()
    files_path:list[str] = get_files_path(work_month_path)
    user:dict = {"name": user, "passwd": passwd}
    start(files_path, work_month, user, data, window, status)


def upload_item_from(routine: Siga, file_path: str) -> None:
    if routine.file_upload(file_path):
        SUCCESSFUL_SENT.append(file_path)
    else:
        FAIL_SENDING.append(file_path)


def save_item(routine: Siga, file_path: str, item: dict, status: InsertionStatus) -> None:
    if routine.save(item):
        status.set_finished(True)
        print(f"{item['file-name']} salvo com sucesso")

    else:
        print(f"falha em salvar: {item['file-name']}")
        status.set_fail_cause(save_error_msg)
        status.set_failed(True)
        FAIL_SENDING.append(file_path)
        EXISTING_FILES.append(file_path)


def start(files_path: str, work_month: str, 
    user: dict, items_list: list[dict], 
    window: bool, status: InsertionStatus) -> None:
    
    username: str = user["name"]
    passwd: str = user["passwd"]

    selenium: Selenium = Selenium(ccb_siga, window)
    status.set_starting()

    for item in items_list:
        selenium.start()
        siga: Siga = Siga(selenium.get_driver())
        
        if siga.login(username, passwd):
            sleep(10)
            siga.change_work_month_date(work_month)
            sleep(4)
            siga.open_tesouraria()
            sleep(2)

            if item["insert-type"] == "MOVINT":
                set_initial_status(item, status)
                movint_insertion(siga, item, status)

            if item["insert-type"] == "DEBT":
                debt_insertion(siga, selenium, files_path, items_list, item, status)

        else:
            status.set_access_error(access_error_msg)
            selenium.close()
            return False

        selenium.close()

    move_files(files_path, SUCCESSFUL_SENT+EXISTING_FILES)
    status.set_finished_all()


def movint_insertion(routine: Siga, item: dict, status: InsertionStatus) -> None:
    if routine.new_intern_transaction(item):
        file_path = get_file_path(item["file-name"])

        if file_path is not None:
            upload_item_from(routine, file_path)
            sleep(3)
            save_item(routine, file_path, item, status)


def debt_insertion(routine: Siga, selenium: Selenium, 
    files_path: list[str], data: list, item: list[dict], 
    status: InsertionStatus) -> None:
    
    if routine.new_debt():
        set_initial_status(item, status)
        
        if routine.debt(item):
            file_path = get_file_path(files_path, item["file-name"])
            
            if file_path is not None:
                upload_item_from(routine, file_path)
                sleep(3)
                save_item(routine, file_path, item, status)
        else:
            selenium.close()
            sleep(5)
            data = [
                item for item in data 
                if not item["file-name"] 
                in SUCCESSFUL_SENT
            ]
            start(data)
    else:
        status.set_insertion_error(insert_error_msg)
        selenium.close()
        return False


def move_files(path: str, success: list) -> None:
    for file in path:
        if file in success:
            basedir: str = file[:file.rfind("/")]
            create_dir(basedir, "Lancados")
            move_file_to(f"{basedir}/Lancados/", file)
