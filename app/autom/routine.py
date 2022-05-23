import os
from time import sleep

from app.autom.main import Selenium
from app.autom.strings import ccb_siga
from app.autom.siga import Siga
from app.autom.msgs import *

from app.config.credentials import Credential

from app.utils.main import InsertionStatus
from app.utils.filemanager import create_dir
from app.utils.filemanager import get_file_location
from app.utils.filemanager import move_file_to
from app.utils.filemanager import get_files_path

from app.execlogs.notifications import *
from app.data.main import check_name_pattern

from app.config.itemsdb import set_inserted_item

SUCCESSFUL_SENT: list = []
FAIL_SENDING   : list = []
EXISTING_FILES : list = []


def set_initial_status(current: dict, status: InsertionStatus) -> None:
    status.set_current(current)
    status.set_finished(False)
    status.set_failed(False)
    status.set_started()


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
    routine.file_upload(file_path)


def save_item(routine: Siga, file_path: str, item: dict,
    status: InsertionStatus) -> None:
    
    if routine.save(item):
        if file_path is not None:
            SUCCESSFUL_SENT.append(file_path)
        status.set_finished(True)
        set_inserted_item(item)
        insertion_success_notification(item)

    else:
        status.set_fail_cause(save_error_msg)
        status.set_failed(True)
        if file_path is not None:
            FAIL_SENDING.append(file_path)
            EXISTING_FILES.append(file_path)
        document_already_exists_notification(item)


def start(files_path: list, work_month: str, 
    user: dict, items_list: list, 
    no_window: bool, status: InsertionStatus) -> None:
    
    username: str = user["name"]
    passwd: str = user["passwd"]

    selenium: Selenium = Selenium(ccb_siga, no_window)
    status.set_starting()

    for item in items_list:
        set_initial_status(item, status)

        if check_name_pattern(item):
            if selenium.start():
                siga: Siga = Siga(selenium.get_driver())
                
                if siga.login(username, passwd):
                    sleep(10)
                    siga.change_work_month_date(work_month)
                    sleep(4)
                    siga.open_tesouraria()
                    sleep(2)

                    if item["insert-type"] == "MOVINT":
                        if movint_insertion(siga, item, status):
                            status.set_finished(True)

                    if item["insert-type"] == "DEBT":
                        if debt_insertion(siga, files_path, item, status):
                            status.set_finished(True)

                else:
                    login_error_notification()
                    status.set_access_error(login_error_msg)
                    selenium.close()
                    break
                sleep(3)
                selenium.close()
            else:
                access_error_notification()
                status.set_access_error(access_error_msg)
                FAIL_SENDING.append(item)
                status.set_failed(True)
                status.set_fail_cause("Não foi possível acessar o sistema")
                status.set_failed_all()
                sleep(3)
                break
        else:
            name_pattern_error_notification(item)
            FAIL_SENDING.append(item)
            status.set_failed(True)
            status.set_fail_cause("O padrão de nomeação não foi reconhecido")
            sleep(2)
    # -----------------------------------------------------------------------------
    if status.errors["access_error"] is not None:
        return status.set_failed_all()

    if len(FAIL_SENDING) > 0 and len(SUCCESSFUL_SENT) > 0:
        sleep(2)
        status.set_finished_all()
        status.set_finished_all_with_exceptions()

    elif len(FAIL_SENDING) > 0 and len(SUCCESSFUL_SENT) == 0:
        sleep(2)
        status.set_finished_all()
        status.set_failed_all()

    else:
        sleep(2)
        status.set_finished_all()
        
    move_files(files_path, SUCCESSFUL_SENT+EXISTING_FILES)


def movint_insertion(routine: Siga, item: dict, status: InsertionStatus) -> bool:
    if routine.new_intern_transaction(item):
        if item.get("type") == "RESG AUTOM" or item.get("type") == "APLICACAO":
            sleep(3)
            save_item(routine, None, item, status)
            return True
        else:
            file_path = get_file_location(item["file-name"])

            if file_path is not None:
                upload_item_from(routine, file_path)
                sleep(3)
                save_item(routine, file_path, item, status)
                return True
            else:
                filepath_error_notification(item)
                status.set_failed(True)
                status.set_fail_cause("Caminho do arquivo não foi encontrado!")
                return False

    return False


def debt_insertion(routine: Siga, files_path: list, item: dict, 
    status: InsertionStatus) -> bool:
    
    if routine.new_debt():    
        if routine.debt(item):
            if item.get("type") == "RECIBO" and item.get("hist-1") == "012":
                sleep(3)
                save_item(routine, None, item, status)
                return True

            file_path = get_file_location(files_path, item["file-name"])
            
            if file_path is not None:
                upload_item_from(routine, file_path)
                sleep(3)
                save_item(routine, file_path, item, status)
                return True
                
            else:
                filepath_error_notification(item)
                status.set_failed(True)
                status.set_fail_cause("Caminho do arquivo não foi encontrado!")
                return False
        else:
            insertion_error_notification(item)
            status.set_failed(True)
            status.set_fail_cause("Erro ao inserir dados do lançamento.")
            return False
    else:
        start_insertion_error_notification()
        status.set_failed(True)
        status.set_fail_cause("Não foi possível abrir rotina de despesas.")
        status.set_insertion_error(insert_error_msg)
    
    return False



def move_files(path: list, success: list) -> None:
    for file in path:
        if file in success:
            basedir: str = None
            if "\\" in file:
                basedir = file[:file.rfind("\\")]
            else:
                basedir = file[:file.rfind("/")]

            create_dir(basedir, "Lancados")
            sent_path: str = os.path.join(basedir, "Lancados")
            move_file_to(sent_path, file)

