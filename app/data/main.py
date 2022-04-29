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
        data = data.upper()

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
            and not data.count("_") == 2 and not ":" in data\
            and not "DP" in data and not "RC" in data and not "R$" in data:
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

        # despesas gerais
        file_data_list: list[dict] = [
            _ for _ in [
                get_data_from_filename(BaseModel(), file) 
                for file in files
            ]
            if _["expenditure"] is not None
            and _["expenditure"] in accepted_accounts
        ]
        # ------------------------------------------------------------

        # movimentação interna
        for file in files:
            modelized_file = get_data_from_filename(Model1415(), file)
            
            if modelized_file.get("orig-account") is not None\
                and modelized_file.get("dest-account") is not None\
                and modelized_file.get("complement") is not None:
                file_data_list.append(modelized_file)
        # -------------------------------------------------------------
        return file_data_list
    return []


def move_classified_files_to_sist_path(
    path: str, file: dict) -> bool:
    
    files: list[str] = get_unclassified_files_from(path)
    keys: list = file.keys()

    base_account: str = None
    sub_account: str = None
    base_account_path: str = None
    filename: str = None

    work_month: str = "-".join(file["date"])[3:]
    work_month_path: str = os.path.join(sist_path, work_month)

    if not os.path.exists(work_month_path):
        set_initial_struct_dirs(work_month_path)

    # despesas gerias
    if "expenditure" in keys:
        if file["expenditure"] is not None:
            base_account = file["cost-account"]
            sub_account = file["expenditure"]
            base_account_path = os.path.join(sist_path, work_month, base_account)

            for item in files:
                if file["file-name"] in item and  ":".join(file["date"]) in item\
                    or "_".join(file["date"]) in item and file["emitter"] in item\
                    and file["value"] in item:
                    filename = item
    # --------------------------------------------------------------------------------

    # movimentação interna
    if "orig-account" in keys and "dest-account" in keys\
        and "insert-type" in keys:
        if file.get("insert-type") == "MOVINT":
            base_account = file["dest-account"]
            sub_account = "1415"
            base_account_path = os.path.join(sist_path, work_month, base_account)

            for item in files:
                if file["file-name"] in item and ":".join(file["date"]) in item\
                    or "_".join(file["date"]) in item and file["value"] in item\
                    or file["complement"] in item:
                    filename = item
    # --------------------------------------------------------------------------------
    
    if not os.path.exists(base_account_path) or filename is None:
        return False

    sub_account_path: list = [
        p for p in os.listdir(base_account_path)
        if sub_account in p    
    ][0]

    base_account_path = os.path.join(base_account_path, sub_account_path)
    filepath = os.path.join(path, filename)
    return copy_file_to(base_account_path, filepath)


def check_name_pattern(item: dict) -> bool:
    if item["insert-type"] == "DEBT":
        if len(item["date"]) == 3 and item["value"] is not None\
            and item["num"] is not None and item["expenditure"] is not None\
            and item["emitter"] is not None:

            # se for pagamento com dinheiro, e não com cheque
            if item["cost-account"] == "1000" and item["doc-num"] is None\
                and item["check-num"] == None:
                return True

            # se for pagamento com cheque, e não um débito automático
            if item["cost-account"] == "1010" and item["doc-num"] is None\
                and item["check-num"] is not None:
                return True

            # se for débito automático, e não um pagamento com cheque
            if item["cost-account"] == "1010" and item["check-num"] is None\
                and item["doc-num"] is not None:
                return True

    if item["insert-type"] == "MOVINT":
        # se for retirada do banco para o caixa, ou da aplicação para o banco
        if item["orig-account"] == "1010" and item["dest-account"] == "1000"\
            or item["orig-account"] == "1033" and item["dest-account"] == "1010"\
            and item["doc-num"] is not None and item["complement"] is not None\
            and str(item["type"]).upper() == "SAQ" and len(item["date"]) == 3\
            and item["value"] is not None:
            return True
        
        # Verificações futuras
    
    return False
