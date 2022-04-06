from time import sleep
import os

from autom.main import Selenium
from autom.strings import ccb_siga
from autom.siga import Siga

from config.credentials import Credential

from utils.filemanager import create_dir, get_files_path, move_file_to



def insert_debt(work_month: str, work_month_path:str, data: list) -> dict:
    selenium = Selenium(ccb_siga)
    selenium.start()
    siga = Siga(selenium.get_driver())
    
    files_sent_successfull = []
    files_not_sent = []
    user, passw = Credential().get_user_credentials()
    files_path = get_files_path(work_month_path)

    sleep(2)
    
    if siga.login(user, passw):
        sleep(10)
        siga.change_work_month_date(work_month)
        sleep(5)
        siga.open_tesouraria()
        sleep(4)

        if siga.new_debt():
            for debt in data:
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
                        if len(data) > 1:
                            print("\n\n\nSalvando e iniciando novo lançamento..\n\n\n")
                            if siga.save_and_new_debt(debt):
                                print(f"{debt['file-name']}: salvo com sucesso.")
                        else:
                            print("\n\n\nSalvando lançamento..\n\n\n")
                            if siga.save_debt(debt):
                                print(f"{debt['file-name']}: salvo com sucesso.")
                sleep(10)


    for file in files_path:
        if file in files_sent_successfull:
            basedir = file[:file.rfind("/")]
            create_dir(basedir, "Lancados")
            move_file_to(f"{basedir}/Lancados/", file)

    selenium.close()
    return {"success": files_sent_successfull, "error": files_not_sent}


if __name__ == "__main__":
    pass