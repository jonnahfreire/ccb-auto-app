import os

from models import debt_models
from models.debt_models import *

from config.globals import sist_path, extensions

from utils.main import get_debt_models_list
from utils.filemanager import move_file_to


def get_data_from_filename(model, file: str) -> dict:
    model.file_name = file.split("-")[0].strip()
    file_data = [os.path.splitext(f.strip())[0] for f in file.split("-")]

    for data in file_data:

        if len(data) > 0 and "NF" in data or "NF RC" in data \
            or "CF" in data or "CF RC" in data or "CP" in data\
            or "CP RC" in data:
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

        if len(data) > 0 and "CH" in data:
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
        
        if len(data) > 0 and "CH" in data or "DB AT" in data:
            model.cost_account = "1010"

        if len(data) > 0 and not data[:3] == "05_":
            model.cost_center = "ADM"

        if len(data) > 0 and not "NF" in data\
            and not "CF" in data and not "CH" in data\
            and not "DB AT" in data and not "05_" in data\
            and not data.count("_") == 2 and not "DP" in data:
            model.emitter = data.strip()
        
        if len(data) > 0 and "DP" in data:
            model.expenditure = data.replace("DP", "").strip()

    return model.get_mapped_data()




def get_modelized_debts(debt_list: list[dict]) -> list[dict]:
    if not debt_list: return []

    debts_data:list = []
    account_codes:list = get_debt_models_list(debt_models)

    def loop(model, iterator: list):
        for db in iterator:
            debts_data.append(get_data_from_filename(model, db))

    for debt in debt_list:
        model = [eval(f"Model{code}") for code in account_codes if debt.get(code)]
        if model: loop(model[0](), debt.get(model[0].__name__[5:]))

    return debts_data


def file_classify(path: str, work_month:str) -> bool:

    if os.path.exists(path) and work_month is not None:

        files: list[str] = [
            file for file in os.listdir(path)
            if os.path.splitext(file)[1] in extensions
        ]

        file_data_list: list[dict] = [
            get_data_from_filename(BaseModel(), file) 
            for file in files
        ]

        for file in file_data_list:
            if file["expenditure"] is not None:
                base_account = file["cost-account"]
                debt_account = file["expenditure"]

                base_account_path = os.path.join(sist_path, work_month, base_account)

                debt_account_path = [
                    p for p in os.listdir(base_account_path)
                    if debt_account in p    
                ][0]
                base_account_path = os.path.join(base_account_path, debt_account_path)

                filename = [
                    _ for _ in files
                    if file["file-name"] in _
                    and ":".join(file["date"]) in _
                    or "_".join(file["date"]) in _
                    and file["emitter"] in _
                ][0]
                filepath = os.path.join(path, filename)
                move_file_to(base_account_path, filepath)

        return True
    return False



if __name__ == "__main__":
    pass

