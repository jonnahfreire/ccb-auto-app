import os

from config.globals import sist_path
from utils.filemanager import list_files, get_files_by_account
from data.main import get_modelized_debts


def get_data(work_month):

    # if work_month is None: cli_main()
    work_month_path: str = os.path.join(sist_path, work_month.replace("/", "-"))

    files: list = list_files(work_month_path)

    if len(files) > 0:
        debts_1000, debts_1010 = get_files_by_account(files)

        modelized_debts_1000: list[dict] = get_modelized_debts(debts_1000)
        # modelized_debts_1010: list[dict] = get_modelized_debts(debts_1010)

        # all_debts: list[dict] = modelized_debts_1000 + modelized_debts_1010

        return modelized_debts_1000

    return {"data": []}