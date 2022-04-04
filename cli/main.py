import os
from time import sleep

from utils.main import clear
from utils.filemanager import create_struct_dir

from config.credentials import Credential
from config.user import User

from config.globals import WIN

from config.globals import unix_sist_path, struct_dirs


def set_work_month() -> str:
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


def set_initial_user_config() -> None:
    user_credential = Credential()
    user_data = user_credential.get_user_credentials()

    if len(user_data) == 0:
        new_user = input("Informe seu usuário do siga: ").strip()
        new_pass = input("Infrome sua senha do siga: ").strip()
        user = User(new_user, new_pass)
        user_credential.set_user_credential(user.get_user(), user.get_pass())


def set_initial_struct_dirs(work_month_path: str) -> None:
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


def select_initial_routine(debts_1000: list[dict], debts_1010: list[dict]) -> str:
    clear()
    print("\n*** Selecione os lançamentos que deseja efetuar ***\n")
    print("1000 - Caixa 1000")
    print(f"\tEncontrados {len(debts_1000)} arquivos para lançar.\n")
    print("1010 - Banco")
    print(f"\tEncontrados {len(debts_1010)} arquivos para lançar.\n")
    print("\n 1 - Todos\n")

    option = input("Digite o código dos lançamentos: ")
    return option