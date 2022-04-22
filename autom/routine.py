from time import sleep

from autom.main import Selenium
from autom.strings import ccb_siga
from autom.siga import Siga

from config.credentials import Credential

from utils.filemanager import create_dir, get_files_path, move_file_to


class InsertionStatus:

    def __init__(self) -> None:
        self.current: dict = {}
        self.starting: bool = False
        self.started: bool = False
        self.failed: bool = False
        self.finished: bool = False
        self.finished_all: bool = False
        self.failed_all: bool = False
    
    def set_current(self, current: dict):
        self.current = current
    
    def set_starting(self):
        self.starting = True

    def set_started(self):
        self.started = True
    
    def set_failed(self, failed: bool):
        self.failed = failed

    def set_finished(self, finished: bool):
        self.finished = finished
        
    def set_finished_all(self):
        self.finished_all = True

    def set_failed_all(self):
        self.failed_all = True



status: dict =  {}
errors = {}

def insert_debt(work_month: str, work_month_path:str, data: list, window: bool) -> None:
    global status

    if len(data) == 0:
        return
    
    files_sent_successfull = []
    files_not_sent = []
    debt_already_exists = []
    user, passw = Credential().get_user_credentials()
    files_path = get_files_path(work_month_path)
    
    status_obj = InsertionStatus()
    selenium = Selenium(ccb_siga, window)

    def execute(data_list: list[dict]):
        status_obj.set_starting()
        status["starting"] = status_obj.starting

        for debt in data_list:
            selenium.start()
            siga = Siga(selenium.get_driver())
            
            if siga.login(user, passw):
                sleep(10)
                siga.change_work_month_date(work_month)
                sleep(4)
                siga.open_tesouraria()
                sleep(2)

                if siga.new_debt():
                    status_obj.set_current(debt)
                    status_obj.set_finished(False)
                    status_obj.set_failed(False)
                    status_obj.set_started()

                    status["current"] = status_obj.current
                    status["finished"] = status_obj.finished
                    status["failed"] = status_obj.failed
                    status["started"] = status_obj.started
                    
                    if siga.debt(debt):
                        file_name = debt["file-name"]
                        file_path = None

                        for fp in files_path:
                            if file_name in fp:
                                file_path = files_path[files_path.index(fp)]

                        if file_path is not None:
                            if siga.file_upload(file_path):
                                files_sent_successfull.append(file_path)
                            else:
                                files_not_sent.append(file_path)

                            sleep(3)
                            if siga.save_debt(debt):
                                status_obj.set_finished(True)
                                status["finished"] = status_obj.finished

                            else:
                                status["fail_cause"] = "Erro ao salvar lançamento. Documento já existe!"
                                status_obj.set_failed(True)
                                status["failed"] = status_obj.failed
                                files_not_sent.append(file_path)
                                debt_already_exists.append(file_path)
                    else:
                        selenium.close()
                        sleep(5)
                        data_list = [
                            debt for debt in data_list 
                            if not debt["file-name"] 
                            in files_sent_successfull
                        ]
                        execute(data_list)

                else:
                    errors["start_insertion_error"] = "Erro ao abrir novo lançamento. Tente novamente!"
                    selenium.close()
                    return False

                sleep(5)

            else:
                errors["access_error"] = "Erro de acesso. Verifique seu usuário!"
                selenium.close()
                return False

            selenium.close()
    
        move_files(files_path, files_sent_successfull+debt_already_exists)
        status_obj.set_finished_all()
        status["finished_all"] = status_obj.finished_all

    execute(data)


def move_files(path: str, success: list) -> None:
    for file in path:
        if file in success:
            basedir: str = file[:file.rfind("/")]
            create_dir(basedir, "Lancados")
            move_file_to(f"{basedir}/Lancados/", file)

            
if __name__ == "__main__":
    pass