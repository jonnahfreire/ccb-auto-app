from time import sleep

from app.autom.main import Selenium
from app.autom.strings import ccb_siga
from app.autom.siga import Siga
from app.autom.msgs import *

from app.config.credentials import Credential

from app.utils.main import InsertionStatus
from app.utils.filemanager import create_dir
from app.utils.filemanager import get_files_path, move_file_to

from app.execlogs.notifications import *
from app.data.main import check_name_pattern

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

    else:
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
                if movint_insertion(siga, item, status):
                    status.set_finished(True)

            if item["insert-type"] == "DEBT":
                set_initial_status(item, status)
                if debt_insertion(siga, files_path, item, status):
                    status.set_finished(True)

        else:
            insert_notification({
                "icon": "danger",
                "header": "Não foi possível logar no sistema.",
                "title": "ccb-auto: não conseguiu autenticar usuário.",
                "message": "Verifique seu acesso, ou redefina os dados de acesso."
            })
            status.set_access_error(access_error_msg)
            selenium.close()
            break
        sleep(3)
        selenium.close()


    if status.errors["access_error"] is not None:
        return status.set_failed_all()

    move_files(files_path, SUCCESSFUL_SENT+EXISTING_FILES)
    status.set_finished_all()


def movint_insertion(routine: Siga, item: dict, status: InsertionStatus) -> bool:
    if check_name_pattern(item):
        if routine.new_intern_transaction(item):
            file_path = get_file_path(item["file-name"])

            if file_path is not None:
                upload_item_from(routine, file_path)
                sleep(3)
                save_item(routine, file_path, item, status)
                return True
    else:
        insert_notification({
            "icon": "danger",
            "header": "Não foi possível iniciar lançamento.",
            "title": f'{item["file-name"]} - R$ {item["value"]}',
            "message": "O padrão de nomeação não foi reconhecido"
        })
        status.set_failed(True)
        status.set_fail_cause("O padrão de nomeação não foi reconhecido")
        return False


def debt_insertion(routine: Siga, files_path: list[str], item: dict, 
    status: InsertionStatus) -> bool:

    # checar se o padrão de nomeação do arquivo está correto
    if check_name_pattern(item):    
        if routine.new_debt():    
            if routine.debt(item):
                file_path = get_file_path(files_path, item["file-name"])
                
                if file_path is not None:
                    upload_item_from(routine, file_path)
                    sleep(3)
                    save_item(routine, file_path, item, status)
                    return True
                    
                else:
                    insert_notification({
                        "icon": "danger",
                        "header": Notification().header_error,
                        "title": f'{item["file-name"]} - R$ {item["value"]} - DP {item["expenditure"]}',
                        "message": "Caminho do arquivo não foi encontrado!"
                    })
                    status.set_failed(True)
                    status.set_fail_cause("Caminho do arquivo não foi encontrado!")
                    return False
            else:
                insert_notification({
                    "icon": "danger",
                    "header": Notification().header_error,
                    "title": f'{item["file-name"]} - R$ {item["value"]} - DP {item["expenditure"]}',
                    "message": "Erro ao inserir dados. Contate o desenvolvedor!"
                })
                status.set_failed(True)
                status.set_fail_cause("Erro ao inserir dados do lançamento.")
                return False
        else:
            insert_notification({
                "icon": "danger",
                "header": "Não foi possível iniciar lançamento.",
                "title": "ccb-auto: não foi possível abrir rotina de despesas.",
                "message": "Erro de rotina. Contate o desenvolvedor!"
            })
            status.set_failed(True)
            status.set_fail_cause("Não foi possível abrir rotina de despesas.")
            status.set_insertion_error(insert_error_msg)
            return False
    else:
        insert_notification({
            "icon": "danger",
            "header": "Não foi possível iniciar lançamento.",
            "title": f'{item["file-name"]} - R$ {item["value"]} - DP {item["expenditure"]}',
            "message": "O padrão de nomeação não foi reconhecido"
        })
        status.set_failed(True)
        status.set_fail_cause("O padrão de nomeação não foi reconhecido")
        return False


def move_files(path: str, success: list) -> None:
    for file in path:
        if file in success:
            basedir: str = file[:file.rfind("/")]
            create_dir(basedir, "Lancados")
            move_file_to(f"{basedir}/Lancados/", file)

