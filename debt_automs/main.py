import os

from config.globals import struct_dirs
from document_models import models
from document_models.models import *

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

        elif len(data) > 0 and "05_" in data:
            model.cost_center = data.replace("_", "-").strip()

        elif len(data) > 0 and "CH" in data:
            model.check_num = data.replace("CH", "").strip()
            model.payment_form = "CHEQUE"
            model.hist2 = "011" # CH Nº
            model.cost_account = "1010"

        elif len(data) > 0 and "DB AT" in data:
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


        elif len(data) > 0 and ":" in data:
            model.date = data.split(":")

        elif len(data) > 0 and "R$" in data:
            model.value = data.replace("R$", "").strip()
        
        else:
            model.emitter = data.strip()

    return model.get_mapped_data()


def get_class_list_by_module(module):
    md = module.__dict__
    return [
        md[c] for c in md if (
            isinstance(md[c], type) and md[c].__module__ == module.__name__
        )
    ]


def get_mapped_models(models) -> list[dict]:
    return [
        _class.__name__[5:]
        for _class in get_class_list_by_module(models)    
    ][1:]


def get_modelized_data(debt_list: list) -> list[dict]:
    if not debt_list: return []

    debts_data:list = []
    account_codes:list = get_mapped_models(models)
    
    def loop(model, iterator: list):
        for db in iterator:
            debts_data.append(get_data_from_filename(model, db))

    for debt in debt_list:
        model = [eval(f"Model{code}") for code in account_codes if debt.get(code)][0]
        if model: loop(model(), debt.get(model.__name__[5:]))
    
    return debts_data


if __name__ == "__main__":
    pass