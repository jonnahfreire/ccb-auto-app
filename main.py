import os

from data.main import get_modelized_debts
from models.debt_models import *

from utils.filemanager import *

from execlogs.logs import *
from config.globals import unix_sist_path
from cli.main import *
from autom.routine import insert_debt


def main():
    set_initial_user_config()
    
    work_month = set_work_month()
    work_month_path = os.path.join(unix_sist_path, work_month.replace("/", "-"))

    set_initial_struct_dirs(work_month_path)

    clear()
    files = list_files(work_month_path)
    debts_1000, debts_1010 = get_files_by_account(files)

    modelized_debts_1000 = get_modelized_debts(debts_1000)
    modelized_debts_1010 = get_modelized_debts(debts_1010)

    all_debts = modelized_debts_1000 + modelized_debts_1010


    option = select_initial_routine(modelized_debts_1000, modelized_debts_1010)

    if option.strip() == "1000":
        insert_debt(work_month, work_month_path, modelized_debts_1000)

    elif option.strip() == "1":
        insert_debt(work_month, work_month_path, all_debts)

    elif option == "1010":
        insert_debt(work_month, work_month_path, modelized_debts_1010)

    clear_logs()
if __name__ == "__main__":
    main()