import os
from time import sleep
import tabula

from app.models import models
from app.models.models import *

from app.config.globals import extensions, accepted_accounts
from app.config.paths import syspath

from app.utils.main import get_items_models_list
from app.utils.filemanager import copy_file_to, select_file
from app.utils.filemanager import select_file
from app.utils.filemanager import set_initial_struct_dirs
from app.utils.filemanager import get_month_directories
from app.utils.filemanager import get_all_files_path
from app.utils.filemanager import list_files
from app.utils.filemanager import get_files_by_account
from app.utils.filemanager import get_file_location 

from app.config.itemsdb import set_item
from app.config.itemsdb import get_all_items
from app.config.itemsdb import get_extract_items

from app.execlogs.notifications import document_already_inserted
from app.execlogs.notifications import document_pattern_not_match



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
        self.extract_month: str = None

        self.__get_extract_data()
        self.__set_extract_month()
        
    def __get_extract_data(self) -> None:
        try:
            df = tabula.read_pdf(self.path, pages = "all")
            data = [str(row).splitlines() for row in df]

            for page in range(len(data)):
                self.get_extract_modelized_data(data, page)
            
        except Exception as JavaNotFoundError:
            print("Error: ", JavaNotFoundError)

    # despesas bancárias
    def get_bank_expenditures(self) -> list:
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
    
    def get_modelized_bank_revenues(self):
        modelized_bank_revenues: list[dict] = []
        model = Model1415()
        for item in self.get_bank_revenues():
            try:
                if item.get("desc") == "RESG AUTOM":
                    model.type      = item.get("desc")
                    model.value     = item.get("value")
                    model.doc_num   = item.get("doc-num")
                    model.file_name = item.get("desc")
                    model.date      = item.get("date").split("/")
                    model.transform = "TRANSF. BANCARIA"
                    model.orig_account = "1033"
                    model.dest_account = "1010"
                    model.hist = "031"
                    model.file_type = "pdf"
                    modelized_bank_revenues.append(model.get_mapped_data())
            except AttributeError:
                break
        return modelized_bank_revenues

    def get_modelized_bank_expenditures(self):
        modelized_bank_expenditures: list[dict] = []
        model = Model3030()
        model2 = Model002()
        for item in self.get_bank_expenditures():
            try:
                values = item.values()
                if "DB CEST PJ" in values or "MANUT CAD" in values:
                    model.date = item.get("date").split("/")

                    model.num = item.get("doc-num")
                    if item.get("desc") == "DEB CEST PJ":
                        model.num = str(int(item.get("doc-num")[0]) + 1) + item.get("doc-num")[1:]

                    model.value     = item.get("value")
                    model.doc_num   = item.get("doc-num")
                    model.file_name = item.get("desc")
                    modelized_bank_expenditures.append(model.get_mapped_data())

                if item.get("desc") == "APLICACAO":
                    model2.value = item.get("value")
                    model2.num   = item.get("doc-num")
                    model2.doc_num   = item.get("doc-num")
                    model2.file_name = item.get("desc")
                    model2.date  = item.get("date").split("/")
                    modelized_bank_expenditures.append(model2.get_mapped_data())  
            except AttributeError:
                break
        return modelized_bank_expenditures

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
                    "date"   : row[0],
                    "doc-num": row[1],
                    "desc"   : row[2],
                    "value"  : row[3],
                    "type"   : row[4]
                }
                model["type"] == "C" and self.revenues.append(model)
                model["type"] == "D" and self.expenditures.append(model)
                if not model in self.extract_data:
                    self.extract_data.append(model)
    
    def __set_extract_month(self) -> str:
        months: list = [
            item.get("date")[3:]
            for item in self.extract_data
            if item.get("date") is not None
        ]
        if len(months) > 0:
            maxm: str = max(months)
            minm: str = min(months)
            if minm is None:
                self.extract_month = maxm
            elif maxm is None:
                self.extract_month = minm
            else:
                self.extract_month = maxm if months.count(maxm) > months.count(minm) else minm
    
    def get_extract_month(self) -> str:
        return self.extract_month

                

def get_extract_data(extract_path: str) -> dict:
    if os.path.isfile(extract_path):
        extract = BankExtractData(extract_path)
        extract_month: str = extract.get_extract_month()
        modelized_extract_expenditures: list[dict] = extract.get_modelized_bank_expenditures()
        modelized_extract_revenues: list[dict] = extract.get_modelized_bank_revenues()

        modelized_extract_data: dict = {
            "month": extract_month.replace("/", "-") if extract_month is not None else None,
            "data": modelized_extract_expenditures + modelized_extract_revenues
        }
        return modelized_extract_data
    return {"month": None, "data": []}


def set_extract_file_data(file: str) -> bool:
    if file is None: return False

    if file is not None:
        data: dict = get_extract_data(file)
        if len(data.get("data")) > 0:
            path: str = os.path.join(syspath, data.get("month"), "1010", "10---EXTRATOS")

            if os.path.exists(path):
                copy_file_to(path, file.replace("/", "\\"))
                
                db_data = get_extract_items()
                data = [item for item in data.get("data") if not item in db_data]
                return set_item(data)
    return False


def data_name_replacer(data: str) -> str:
    return data.replace("CF", "").replace("CF RC", "").replace("NF", "")\
        .replace("NF RC", "").replace("RC", "").replace("CP", "")\
        .replace("CP RC", "").strip()


def get_data_from_filename(model, file: str) -> dict:
    model.file_name = file.split("-")[0].strip()
    model.file_type = os.path.splitext(file)[1][1:]
    file_data = [os.path.splitext(f.strip())[0] for f in file.split("-")]

    for data in file_data:
        data = data.upper()

        if len(data) > 0 and "CH SAQ" in data:
            model.doc_num = data.split()[-1].strip()

        if len(data) > 0 and "SUPRIMENTO CAIXA" in data\
            or "SUPRIMENTO DE CAIXA" in data or "SUPRIMENTO" in data:
            model.transform = "CHEQUE"
            model.orig_account = "1010"
            model.dest_account = "1000"
            model.complement = data
            model.receiver = "Congregação Cristã no Brasil"
            model.hist = "032"

        if len(data) > 0 and data.split()[0].strip() == "RC":
            model.type = "RECIBO"
            model.hist1 = "024"
            model.hist2 = "024"
            model.num = data_name_replacer(data)

        if len(data) > 0 and "NF" in data or "NF RC" in data \
            or "CF" in data or "CF RC" in data or "CP" in data\
            or "CP RC" in data:
            model.type = "NOTA FISCAL"
            model.hist1 = "021"
            model.hist2 = "023"
            model.num = data_name_replacer(data)
                            
        if len(data) > 0 and data[:3] == "05_":
            model.cost_center = data.replace("_", "-").strip()

        if len(data) > 0 and data.split()[0].strip() == "CH":
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
        
        if len(data) > 0 and data.split()[0].strip() == "CH" or "DB AT" in data:
            model.cost_account = "1010"

        if len(data) > 0 and not data[:3] == "05_":
            model.cost_center = "ADM"

        if len(data) > 0 and not "NF" in data\
            and not "CF" in data and not data.split()[0].strip() == "CH"\
            and not "DB AT" in data and not "05_" in data\
            and not data.count("_") == 2 and not ":" in data\
            and not "DP" in data and not "RC" in data and not "R$" in data:
            model.emitter = data.strip()
        
        if len(data) > 0 and not "NF" in data\
            and not "CF" in data and not data.split()[0].strip() == "CH"\
            and not "DB AT" in data\
            and "RC" in data:
            model.type = "RECIBO"
            model.hist1, model.hist2 = "024", "024"
        
        if len(data) > 0 and "DP" in data.upper():
            model.expenditure = data.replace("DP", "").strip()

    return model.get_mapped_data()


def get_modelized_items(items_list: list, files_path: str = None) -> list:
    if not items_list: return []

    items_data:list = []
    account_codes:list = get_items_models_list(models)
    inserted_files: list = []

    for month in get_month_directories():
        [inserted_files.append(item) for item in get_month_inserted_items(month)]

    def loop(model, iterator: list):
        for db in iterator:
            item: dict = get_data_from_filename(model, db)
            
            if isinstance(db, str) and not db in inserted_files:
                if check_name_pattern(item):
                    item["location"] = get_file_location(files_path, item.get("file-name"))
                    items_data.append(item)
                else:
                    document_pattern_not_match(item)
            else:
                document_already_inserted(item)
                
    for item in items_list:
        if isinstance(item, dict):
            model = [eval(f"Model{code}") for code in account_codes if item.get(code)]
            if model: loop(model[0](), item.get(model[0].__name__[5:]))
            del model
        
        if isinstance(item, str):
            splitted_item = os.path.splitext(item)[0].split("-")
            code = [data.split()[1].strip() for data in splitted_item if "DP" in data][0]
            
            if code and code is not None:
                model = eval(f"Model{code}")
                loop(model(), [item])
                del model

    return items_data


def get_unclassified_files_from(path: str) -> list:
    files: list[str] = [
        file for file in os.listdir(path)
        if os.path.splitext(file)[1] in extensions
        and "NF" in file or "RC" in file or "CH" in file\
        or "CP" in file or "CF" in file\
        or "DB AT" in file and "DP" in file and "R$" in file
    ]
    return files


def set_fileitems_data() -> bool:
    months: list = [month for month in os.listdir(syspath) if not "config" in month]
    workings_paths: list = [
        os.path.join(syspath, path) 
        for path in months
        if not ".pdf" in path \
        or not ".png" in path \
        or not ".jpg" in path
    ]

    files: list = [
        file for file in [
            list_files(path) 
            for path in workings_paths
        ]
    ]

    files_path: list = get_all_files_path(workings_paths)
    if len(files) > 0:
        items: list[dict] = []

        for item in files:
            items_1000, items_1010 = get_files_by_account(item)
            
            modelized_items_1000: list[dict] = []
            modelized_items_1010: list[dict] = []

            if len(items_1000) > 0:
                modelized_items_1000 = get_modelized_items(items_1000, files_path)

            if len(items_1010) > 0:
                modelized_items_1010 = get_modelized_items(items_1010, files_path)
                
            items += [file for file in modelized_items_1000 + modelized_items_1010]
        
        items = [item for item in items if not item in get_all_items(return_type="list")]
        return set_item(items)
    return False

    
def get_classified_files(path:str) -> list:
    if isinstance(path, str) and os.path.exists(path):
        files: list[str] = get_unclassified_files_from(path)
        modelized_files: list = get_modelized_items(files)

        return modelized_files
    return []


def move_classified_files(
    path: str, file: dict) -> bool:
    
    files: list[str] = get_unclassified_files_from(path)
    keys: list = file.keys()

    base_account: str = None
    sub_account: str = None
    base_account_path: str = None
    filename: str = None

    work_month: str = "-".join(file["date"])[3:]
    work_month_path: str = os.path.join(syspath, work_month)

    if not os.path.exists(work_month_path):
        set_initial_struct_dirs(work_month_path)
    
    # despesas gerais
    if "expenditure" in keys:
        if file["expenditure"] is not None:
            base_account = file["cost-account"]
            sub_account = file["expenditure"]
            base_account_path = os.path.join(syspath, work_month, base_account)

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
            base_account_path = os.path.join(syspath, work_month, base_account)

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
    if item.get("insert-type") == "DEBT":
        if len(item["date"]) == 3 and item.get("value") is not None\
            and item.get("num") is not None and item.get("expenditure") is not None\
            and item.get("emitter") is not None:

            # se for pagamento com dinheiro, e não com cheque
            if item.get("cost-account") == "1000" and item.get("doc-num") is None\
                and item.get("check-num") == None:
                return True

            # se for pagamento com cheque, e não um débito automático
            if item.get("cost-account") == "1010" and item.get("doc-num") is None\
                and item.get("payment-form") == "CHEQUE" and item.get("check-num") is not None:
                return True

            # se for débito automático, e não um pagamento com cheque
            if item.get("cost-account") == "1010" and item.get("check-num") == None\
                and item.get("payment-form") == "DEBITO AUTOMATICO" and not item.get("doc-num") == None:
                return True

    if item["insert-type"] == "MOVINT":
        if item["type"] == "RESG AUTOM" and item["orig-account"] == "1033"\
            and item["dest-account"] == "1010" and item["doc-num"] is not None\
            and item["value"] is not None and len(item["date"]) == 3:
            return True
        
        if item["type"] == "APLICACAO" and item["orig-account"] == "1010"\
            and item["dest-account"] == "1033" and item["doc-num"] is not None\
            and item["value"] is not None and len(item["date"]) == 3:
            return True

        # se for retirada do banco para o caixa, ou da aplicação para o banco
        if item["orig-account"] == "1010" and item["dest-account"] == "1000"\
            and item["doc-num"] is not None and item["complement"] is not None\
            and str(item["type"]).upper() == "SAQ" and len(item["date"]) == 3\
            and item["value"] is not None:
            return True
        
        # Verificações futuras
    
    return False


def get_month_inserted_items(month: str) -> list:
    sleep(0.3)
    work_month_path: str = os.path.join(syspath, month)

    if not os.path.isdir(work_month_path):
        return []

    dirs: list = os.listdir(work_month_path)
    items_dirs: list = [os.listdir(os.path.join(work_month_path, _dir)) for _dir in dirs]
    
    files: list = []
    for item_dir in items_dirs:
        for _dir in item_dir:
            path_1000: str = os.path.join(syspath, month, "1000", _dir, "Lancados")
            path_1010: str = os.path.join(syspath, month, "1010", _dir, "Lancados")
            
            if os.path.exists(path_1000):
                [files.append(item) for item in os.listdir(os.path.join(path_1000))]
            
            if os.path.exists(path_1010):
                [files.append(item) for item in os.listdir(os.path.join(path_1010))]

        
    return files
