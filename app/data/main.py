import os

from app.models import models
from app.models.models import *

from app.config.globals import sist_path, extensions, accepted_accounts

from app.utils.main import get_items_models_list
from app.utils.filemanager import copy_file_to, set_initial_struct_dirs


def get_data_from_filename(model, file: str) -> dict:
    model.file_name = file.split("-")[0].strip()
    model.file_type = os.path.splitext(file)[1][1:]
    file_data = [os.path.splitext(f.strip())[0] for f in file.split("-")]

    for data in file_data:

        if len(data) > 0 and "CH SAQ" in data:
            model.doc_num = data.split(" ")[-1].strip()

        if len(data) > 0 and "SUPRIMENTO CAIXA" in data\
            or "SUPRIMENTO DE CAIXA" in data or "SUPRIMENTO" in data:
            model.transform = "CHEQUE"
            model.orig_account = "1010"
            model.dest_account = "1000"
            model.complement = data
            model.receiver = "Congregação Cristã no Brasil"
            model.hist = "032"

        if len(data) > 0 and "NF" in data or "NF RC" in data \
            or "CF" in data or "CF RC" in data or "CP" in data\
            or "CP RC" in data or "RC" in data:
            model.type = "NOTA FISCAL"
            model.hist1 = "021"
            model.hist2 = "023"
            model.num = data.replace("CF", "")\
                            .replace("CF RC", "")\
                            .replace("NF", "")\
                            .replace("NF RC", "")\
                            .replace("RC", "")\
                            .replace("CP", "")\
                            .replace("CP RC", "").strip()

        if len(data) > 0 and data[:3] == "05_":
            model.cost_center = data.replace("_", "-").strip()

        if len(data) > 0 and data.split(" ")[0].strip() == "CH":
            model.check_num = data.replace("CH", "").strip()
            model.payment_form = "CHEQUE"
            model.hist2 = "011" # CH Nº
            model.cost_account = "1010"

        if len(data) > 0 and "DB AT" in data:
            model.type = "NOTA FISCAL"
            model.num = data.replace("DB AT", "")\
                            .replace("LUZ", "")\
                            .replace("FONE", "").strip()
            model.hist1 = "021"
            model.hist2 = "007" #"AVISO DE DÉBITO"
            model.cost_account = "1010"
            model.payment_form = "DEBITO AUTOMATICO"
            if "LUZ" in data:
                model.doc_num = "200118"
            if "FONE" in data:
                model.doc_num = "300200"

        if len(data) > 0 and ":" in data:
            model.date = data.split(":")
        
        if len(data) > 0 and data.count("_") == 2:
            model.date = data.strip().split("_")

        if len(data) > 0 and "R$" in data:
            model.value = data.replace("R$", "").strip()
        
        if len(data) > 0 and data.split(" ")[0].strip() == "CH" or "DB AT" in data:
            model.cost_account = "1010"

        if len(data) > 0 and not data[:3] == "05_":
            model.cost_center = "ADM"

        if len(data) > 0 and not "NF" in data\
            and not "CF" in data and not data.split(" ")[0].strip() == "CH"\
            and not "DB AT" in data and not "05_" in data\
            and not data.count("_") == 2 and not "DP" in data\
            and not "RC" in data:
            model.emitter = data.strip()
        
        if len(data) > 0 and not "NF" in data\
            and not "CF" in data and not data.split(" ")[0].strip() == "CH"\
            and not "DB AT" in data\
            and "RC" in data:
            model.type = "RECIBO"
            model.hist1, model.hist2 = "024", "024"
        
        if len(data) > 0 and "DP" in data:
            model.expenditure = data.replace("DP", "").strip()

    return model.get_mapped_data()


def get_modelized_items(items_list: list[dict]) -> list[dict]:
    if not items_list: return []

    items_data:list = []
    account_codes:list = get_items_models_list(models)

    def loop(model, iterator: list):
        for db in iterator:
            items_data.append(get_data_from_filename(model, db))

    for item in items_list:
        model = [eval(f"Model{code}") for code in account_codes if item.get(code)]
        if model: loop(model[0](), item.get(model[0].__name__[5:]))

    return items_data


def get_unclassified_files_from(path: str) -> list:
    files: list[str] = [
        file for file in os.listdir(path)
        if os.path.splitext(file)[1] in extensions
    ]
    return files


def get_classified_files(path:str) -> list[dict]:
    if isinstance(path, str) and os.path.exists(path):
        files: list[str] = get_unclassified_files_from(path)

        file_data_list: list[dict] = [
            _ for _ in [
                get_data_from_filename(BaseModel(), file) 
                for file in files
            ]
            if _["expenditure"] is not None
            and _["expenditure"] in accepted_accounts
        ]

        return file_data_list
    return []


def move_classified_files_to_sist_path(
    path: str, file: list[dict]) -> bool:
    
    files: list[str] = get_unclassified_files_from(path)

    if file["expenditure"] is not None:
        base_account: str = file["cost-account"]
        debt_account: str = file["expenditure"]
        work_month: str = "-".join(file["date"])[3:]

        work_month_path: str = os.path.join(sist_path, work_month)
        if not os.path.exists(work_month_path):
            set_initial_struct_dirs(work_month_path)

        base_account_path: str = os.path.join(sist_path, work_month, base_account)

        if not os.path.exists(base_account_path):
            return False

        debt_account_path: list = [
            p for p in os.listdir(base_account_path)
            if debt_account in p    
        ][0]
        base_account_path = os.path.join(base_account_path, debt_account_path)


        filename: str = [
            _ for _ in files
            if file["file-name"] in _
            and ":".join(file["date"]) in _
            or "_".join(file["date"]) in _
            and file["emitter"] in _
            and file["value"] in _
        ][0]
        filepath = os.path.join(path, filename)
        return copy_file_to(base_account_path, filepath)
    
    return False


if __name__ == "__main__":
    pass

