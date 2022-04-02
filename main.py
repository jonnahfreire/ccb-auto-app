from time import sleep
from debt_automs.main import *

from document_models.models import *
from utils.main import WIN, clear

from autom.paths import ccb_siga
from autom.main import Selenium
from autom.routes import Siga

from config.user import User
from config.credentials import Credential

from config.globals import get_files_path, unix_sist_path, struct_dirs


def create_struct_dir(path: str, struct_dirs: list, top_dir: str) -> None:
    try:
        os.makedirs(os.path.join(path, top_dir))
        
        for struct in struct_dirs:
            os.mkdir(os.path.join(path, top_dir, struct))

    except FileExistsError as e:
        print(e)


def set_work_month():
    clear()
    work_month = input("Selecione o mês de trabalho Ex: 01/2022: ").strip()

    if len(work_month) == 7 \
        and "/" in work_month \
        or "-" in work_month \
        and work_month.replace("/", "").isdigit() \
        or work_month.replace("-", "").isdigit():
        
        return work_month

    print("Houve um erro. Digite novamente o mês de trabalho.")
    print("Ex: 01/2022")
    sleep(7)
    set_work_month()


def list_files(base_path: str) -> list:
    base_accounts = []

    if os.path.exists(base_path):
        dirs = os.listdir(base_path)
        base_accounts = [a for a in dirs]

    account_files = []
    for account in base_accounts:
        accounts = os.listdir(os.path.join(base_path, account))

        for acc in accounts:
            files_by_account = os.listdir(os.path.join(base_path, account, acc))
            if files_by_account:
                account_files.append({account: {acc: files_by_account}})

    return account_files


def get_files_by_account(files: list) -> tuple[list]:
    debts_1000, debts_1010 = [], []

    for debts in files:
        for key in debts.keys():
            if key == "1000":
                debts_1000.append(debts[key])

            elif key == "1010":
                debts_1010.append(debts[key])
        
    return debts_1000, debts_1010


def get_modelized_data(debt_list: list) -> list:
    debt_data = []
    
    for debt in debt_list:
        debt_3026 = debt.get("3026")
        debt_3008 = debt.get("3008")
        debt_3014 = debt.get("3014")
        
        def loop(model, iterator: list):
            for db in iterator:
                debt_data.append(get_data_from_filename(model, db))

        if debt_3026:
            loop(Model3026(), debt_3026)
        if debt_3008:
            loop(Model3008(), debt_3008)
        if debt_3014:
            loop(Model3014(), debt_3014)
    
    return debt_data


def insert_debt(work_month: str, work_month_path:str, data: list) -> list:
    selenium = Selenium(ccb_siga)
    selenium.start()
    siga = Siga(selenium.get_driver())
    
    files_sent_successfull = []
    files_not_sent = []
    user, passw = Credential().get_user_credentials()
    files_path = get_files_path(work_month_path)

    sleep(2)

    if siga.login(user, passw):
        sleep(10)
        siga.change_work_month_date(work_month)
        sleep(5)
        siga.open_tesouraria()
        sleep(4)
        siga.new_debt()

        for debt in data:
            siga.debt_3026(debt)

            file_name = debt["file-name"]
            file_path = None

            for fp in files_path:
                if file_name in fp:
                    file_path = files_path[files_path.index(fp)]

            if file_path is not None:
                if siga.file_upload(file_path):
                    files_sent_successfull.append(file_path)
                else:
                    files_not_sent.append(file_path)

                sleep(3)
                if len(data) > 0:
                    print("\n\n\nSalvando e iniciando novo lançamento..\n\n\n")
                    siga.save_and_new_debt()
                else:
                    print("\n\n\nSalvando lançamento..\n\n\n")
                    siga.save_debt()

            sleep(10)

    selenium.close()
    return files_sent_successfull, files_not_sent


def reset_db():
    Credential().reset_all()


def main():
    user_credential = Credential()
    user_data = user_credential.get_user_credentials()
    if len(user_data) == 0:
        new_user = input("Informe seu usuário do siga: ").strip()
        new_pass = input("Infrome sua senha do siga: ").strip()
        user = User(new_user, new_pass)
        user_credential.set_user_credential(user.get_user(), user.get_pass())
    
    work_month = set_work_month()
    work_month_path = os.path.join(unix_sist_path, work_month.replace("/", "-"))

    if not WIN:
        if not os.path.exists(unix_sist_path):
            os.mkdir(unix_sist_path)
        
        # Create ccb-autom/03-2022 Ex.
        if not os.path.exists(work_month_path):
            os.makedirs(work_month_path)
        
            for struct in struct_dirs:
                create_struct_dir(work_month_path, struct[1:], struct[0])
        else:
            # Windows implementation
            pass


    files_by_account = list_files(work_month_path)
    debts_1000, debts_1010 = get_files_by_account(files_by_account)

    modelized_data_1000 = get_modelized_data(debts_1000)
    modelized_data_1010 = get_modelized_data(debts_1010)

    files_data = modelized_data_1000 + modelized_data_1010
    
    print(modelized_data_1000[2])
    
    # return
    # return

    clear()
    print("\n*** Selecione os lançamentos que deseja efetuar ***\n")
    print("1000 - Caixa 1000")
    print(f"\tEncontrados {len(modelized_data_1000)} arquivos para lançar.\n")
    print("1010 - Banco")
    print(f"\tEncontrados {len(modelized_data_1010)} arquivos para lançar.\n")

    print("\n 1 - Todos\n")

    option = input("Digite o código dos lançamentos: ")

    if "1000" in option.strip():
        debt_1000, debt_1010 = insert_debt(work_month, work_month_path, modelized_data_1000)
        print(debt_1000, debt_1010)

    elif "1" in option.strip():
        insert_debt(work_month, work_month_path, files_data)

    elif "1010" in option:
        insert_debt(work_month, work_month_path, modelized_data_1010)


if __name__ == "__main__":
    main()

    modal_header_success_confirm = '/html/body/div[17]/div[3]/a' # Modal que aparece quando confirma o lançamento
    modal_header = '/html/body/div[17]/div[1]' # Modal que aparece quando confirma o lançamento e já existe um documento lançado com o mesmo número
    confirm_modal_header = '/html/body/div[17]/div[3]/a[1]' # Botão de confirmar o modal que aparece quando já existe um lançamento com o mesmo número
    reject_modal_header = '/html/body/div[17]/div[3]/a[2]' # Botão de cancelar o modal que aparece quando já existe um lançamento com o mesmo número