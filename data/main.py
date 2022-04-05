import os

from models import debt_models
from models.debt_models import *

from utils.main import get_class_list_by_module, get_debt_models_list, model_name_exists

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
            and not data.count("_") == 2:
            model.emitter = data.strip()

    return model.get_mapped_data()


def get_modelized_debts(debt_list: list) -> list[dict]:
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


if __name__ == "__main__":
    pass