import os
from time import sleep
import tabula

from app.models import models
from app.models.models import *

from app.config.globals import sist_path, extensions, accepted_accounts

from app.utils.main import get_items_models_list
from app.utils.filemanager import copy_file_to
from app.utils.filemanager import set_initial_struct_dirs
from app.utils.filemanager import get_month_directories

from app.execlogs.notifications import document_already_inserted



class BankExtractData:
    """Extrai os dados a partir do extrato bancário em PDF

    Uso: 
        extract = BankExtractData(extract_path : str)

        data = extract.get_extract_data()

        expenditures = extract.get_bank_expenditures()

        revenues = extract.get_bank_revenues()
    """

    def __init__(self, extract_path: str) -> None:
        self.path: str = extract_path
        self.extract_data: list[dict] = []
        self.expenditures: list[dict] = []
        self.revenues: list[dict] = []

        self.get_extract_data()
        
    def get_extract_data(self) -> list[dict]:
        df = tabula.read_pdf(self.path, pages = "all")
        data = [str(row).splitlines() for row in df]

        for page in range(len(data)):
            self.get_extract_modelized_data(data, page)
        
        return self.extract_data

    # despesas bancárias
    def get_bank_expenditures(self) -> list[dict]:
        if not self.expenditures:
            item = [item for item in self.extract_data if "D" in item.values()]
            self.expenditures.append(item)

        return self.expenditures

    # receitas bancárias
    def get_bank_revenues(self):
        if not self.revenues:
            item = [item for item in self.extract_data if "C" in item.values()]
            self.revenues.append(item)

        return self.revenues

    def get_extract_modelized_data(self, data: list, page: int) -> None:
        data_step1:list = []
        data_step2:list = []
        
        for data in data[page]:
            data_step1.append(data.replace(" ", "-"))

        for data in data_step1:
            if data_step1.index(data) == 1 and page == 1:
                saldo_anterior = data.split("-")[-2]

            if not data_step1.index(data) == 0 and not data_step1.index(data) == 1:
                data_step2.append(
                    [d for d in data.split("-") 
                    if not d == '' and not "NaN" in d
                ][1:-2])

        for data in data_step2:
            row: list[str] = []

            if len(data) == 5 and not "Lançamentos" in data and not "Data" in data and not "APLICACAO" in data:
                row = [data[0], data[1]] + [f"{data[2]} {data[3]}"] + [data[4]]

            elif "APLICACAO" in data: 
                row = data
            
            if len(data) == 6:
                row = [data[0], data[1]] + [f"{data[2]} {data[3]}"] + [data[4], data[5]]

            if len(data) == 7:
                row = [data[0], data[1]] + [f"{data[2]} {data[3]} {data[4]}"] + [data[5], data[6]]

            if len(row) > 0:
                model = {
                    "date" : row[0],
                    "num"  : row[1],
                    "desc" : row[2],
                    "value": row[3],
                    "type" : row[4]
                }
                model["type"] == "C" and self.revenues.append(model)
                model["type"] == "D" and self.expenditures.append(model)
                self.extract_data.append(model)
                


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
            sg_list: list = ["CF", "CF RC", "NF", "NF RC", "RC", "CP", "CP RC"] 
            model.num = [data.replace(sg, "") for sg in sg_list][0].strip()
                            
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
        
        if len(data) > 0 and "DP" in data.upper():
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

        inserted_files: list = []
        for month in get_month_directories():
            [inserted_files.append(item) for item in get_month_inserted_items(month)]

        modelized_files: list = []
        for file in files:
            item: dict = {}
            modelized_db_item: dict = get_data_from_filename(BaseModel(), file)
            modelized_mi_item: dict = get_data_from_filename(Model1415(), file)

            # despesas gerais
            if check_name_pattern(modelized_db_item):
                item = modelized_db_item
            
            #movimentação interna
            if check_name_pattern(modelized_mi_item):
                item = modelized_mi_item

            if not file in inserted_files:
                modelized_files.append(item)
            else:
                document_already_inserted(item)

        file_data_list: list[dict] = []
        for modelized_item in modelized_files:
            # despesas gerais
            if modelized_item["expenditure"] is not None\
               and modelized_item["expenditure"] in accepted_accounts:
               file_data_list.append(modelized_item)
        # ------------------------------------------------------------
            # movimentação interna
            if modelized_item.get("orig-account") is not None\
                and modelized_item.get("dest-account") is not None\
                and modelized_item.get("complement") is not None:
                file_data_list.append(modelized_item)
        # -------------------------------------------------------------
        return file_data_list
    return []


def move_classified_files(
    path: str, file: dict) -> bool:

    if not check_name_pattern(file):
        return False
    
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


def get_month_inserted_items(month: str) -> list:
    sleep(0.3)
    work_month_path: str = os.path.join(sist_path, month)

    if not os.path.isdir(work_month_path):
        return False

    dirs: list = os.listdir(work_month_path)
    items_dirs: list = [os.listdir(os.path.join(work_month_path, _dir)) for _dir in dirs]
    
    files: list = []
    for item_dir in items_dirs:
        for _dir in item_dir:
            path_1000: str = os.path.join(sist_path, month, "1000", _dir, "Lancados")
            path_1010: str = os.path.join(sist_path, month, "1010", _dir, "Lancados")
            
            if os.path.exists(path_1000):
                [files.append(item) for item in os.listdir(os.path.join(path_1000))]
            
            if os.path.exists(path_1010):
                [files.append(item) for item in os.listdir(os.path.join(path_1010))]

        
    return files
