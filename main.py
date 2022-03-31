from time import sleep
from debt_automs.main import *
from autom.main import Selenium
from autom.routes import Siga

from document_models.models import *

from autom.paths import ccb_siga
from dev.config import *

def main():
    files = get_files_from("files/1000/3026")
    file_data = get_data_by_model(model3026, files)

    print(file_data[0])
    
    # for file, i in enumerate(file_data):
    
    if file_data:       
        selenium = Selenium(ccb_siga)
        selenium.start()
        siga = Siga(selenium.get_driver())

        
        sleep(2)
        siga.login(user, passw)
        sleep(5)
        siga.change_work_month_date("03/2022")
        sleep(5)
        siga.open_tesouraria()
        sleep(4)
        siga.new_debt()
        siga.debt_3026(file_data[0])

        file_path = os.path.join(os.getcwd(), f'files/1000/3026/{file_data[0]["file-name"]}')
        siga.file_upload(file_path)

        sleep(100)
        selenium.close()

        
        # selenium.close()

if __name__ == "__main__":
    main()
    # file_path = os.path.join(os.getcwd(), f"files/1000/3026/{0}")
    # print(file_path)
    # files = get_files_from("files/1000/3026")
    # file_data = get_data_by_model(model3026, files)
    # print(file_data[0])
