import os

from data.main import get_modelized_debts
from models.debt_models import *

from utils.filemanager import *
from utils.main import *

from execlogs.logs import *
from config.globals import sist_path
from cli.main import *
from autom.routine import insert_debt

from cli.colors import *
from cli.strings import *



def main():
    
    set_initial_user_config() 
    
    work_month: str = set_work_month()
    if work_month is None: main()
    work_month_path: str = os.path.join(sist_path, work_month.replace("/", "-"))

    set_initial_struct_dirs(work_month_path)
    
    files: list = list_files(work_month_path)

    if len(files) > 0:
        debts_1000, debts_1010 = get_files_by_account(files)

        modelized_debts_1000: list[dict] = get_modelized_debts(debts_1000)
        modelized_debts_1010: list[dict] = get_modelized_debts(debts_1010)

        all_debts: list[dict] = modelized_debts_1000 + modelized_debts_1010
        option: str = select_initial_routine(modelized_debts_1000, modelized_debts_1010)

        if option.strip() == "1000":
            if len(modelized_debts_1000) > 0:
                insert_debt(work_month, work_month_path, modelized_debts_1000)

        elif option == "1010":
            if len(modelized_debts_1010) > 0:
                insert_debt(work_month, work_month_path, modelized_debts_1010)
        
        elif option.strip() == "1":
            if len(all_debts) > 0:
                insert_debt(work_month, work_month_path, all_debts)
        
        
        logs: list = get_execlogs()
        for log in logs:
            sleep(1)
            print(log[1])

    else:
        banner()
        print(no_debts_found.format(work_month_path))
        print(restart)
        sleep(10)


if __name__ == "__main__":
    while True: main()

