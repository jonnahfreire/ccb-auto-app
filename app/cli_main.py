import os

from data.main import get_modelized_items
from models.models import *

from utils.filemanager import *
from utils.main import *

from execlogs.logs import *
from config.globals import sist_path
from cli.main import *
from autom.routine import insert_item

from cli.colors import *
from cli.strings import *

from autom.main import Selenium
from autom.strings import ccb_siga
from autom.siga import Siga

from config.credentials import Credential


def cli_main():
    
    set_initial_user_config() 
    
    work_month: str = "04/2022"#set_work_month()
    if work_month is None: cli_main()
    work_month_path: str = os.path.join(sist_path, work_month.replace("/", "-"))

    set_initial_struct_dirs(work_month_path)
    
    files: list = list_files(work_month_path)

    if len(files) > 0:
        items_1000, items_1010 = get_files_by_account(files)

        modelized_items_1000: list[dict] = get_modelized_items(items_1000)
        modelized_items_1010: list[dict] = get_modelized_items(items_1010)

        all_items: list[dict] = modelized_items_1000 + modelized_items_1010

        for i in all_items: print("\n", i)
        
        # user, passw = Credential().get_user_credentials()

        # selenium = Selenium(ccb_siga, False)
        # selenium.start()
        # siga = Siga(selenium.get_driver())
        
        # if siga.login(user, passw):
        #     # siga.change_work_month_date(work_month)
        #     sleep(10)
        #     # sleep(4)
        #     siga.open_tesouraria()
        #     sleep(2)
            
        #     for item in modelized_items_1000:
        #         siga.new_intern_transaction(item)
        

        # logs: list = get_execlogs()
        # for log in logs: print(log[1])
        # clear_logs()

        # sleep(2000)
        return
        option: str = select_initial_routine(modelized_items_1000, modelized_items_1010)

        if option.strip() == "1000":
            if len(modelized_items_1000) > 0:
                insert_item(work_month, work_month_path, modelized_items_1000, False)
                sleep(10)

        elif option == "1010":
            if len(modelized_items_1010) > 0:
                insert_item(work_month, work_month_path, modelized_items_1010, True)
        
        elif option.strip() == "1":
            if len(all_items) > 0:
                insert_item(work_month, work_month_path, all_items, True)

    else:
        banner()
        print(no_items_found.format(work_month_path))
        print(restart)
        sleep(2)

    logs: list = get_execlogs()
    for log in logs: print(log[1])

    clear_logs()

    
if __name__ == "__main__":
    cli_main()


