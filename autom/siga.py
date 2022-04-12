from time import sleep
import pyautogui

from autom.strings import *
from utils.main import WIN, enter

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from selenium.common.exceptions import NoSuchElementException

from execlogs.logs import *
from cli.colors import *


class Siga:

    def __init__(self, driver) -> None:
        self.driver = driver

    def login(self, user: str, passw: str) -> bool:
        try:
            user_input_user = self.driver.find_element(By.XPATH, input_user)
            user_input_user.click()
            user_input_user.send_keys(user)
            sleep(2)
            user_input_pass = self.driver.find_element(By.XPATH, input_pass)
            user_input_pass.click()
            user_input_pass.send_keys(passw)
            sleep(1)
            login_btn = self.driver.find_element(By.XPATH, login_confirm)
            login_btn.click()
            return True
        except Exception as err:
            insert_execlog(f"{red}Login Error: {yellow}\n\t{err}{bg}\n")
            return False

    def change_work_month_date(self, month: str) -> bool:
        try:
            self.driver.find_element(By.XPATH, work_month_date_select).click()
            sleep(3)
            self.driver.find_element_by_link_text(open_month_date_options).click()
            sleep(2)
            self.driver.find_element(By.XPATH, open_select_month_date).click()
            sleep(2)
            input_month = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen10_search"]')
            input_month.send_keys(month)
            input_month.send_keys(Keys.RETURN)
            sleep(0.5)

            form_ids = ['form-competencias', 'form-executar-programa', 
                        'f-calendar', 'f_main', 'form-competencia', 'f_fecharacessoremoto', 
                        'form-selecionarlocalpadrao', 'form-selecionarlocalidade']

            forms = self.driver.find_elements(By.TAG_NAME, 'form')
            ids = [form.get_attribute("id") for form in forms]

            btn_save_id = [_id for _id in ids if _id not in form_ids][0]
            btn_save_xpath = f'//*[@id="{btn_save_id}"]/div[2]/button'

            self.driver.find_element(By.XPATH, btn_save_xpath).click()

            return True
        except NoSuchElementException as err:
            insert_execlog(f"{red}ChangeWorkMonth Error: {yellow}\n\t{err}{bg}\n")
            sleep(5)
            return False

    def open_tesouraria(self) -> bool:
        try:
            self.driver.find_element(By.XPATH, menu_tesouraria).click()
            sleep(2)
            self.driver.find_element(By.XPATH, caixa_bancos).click()
            return True
        except Exception as err:
            insert_execlog(f"{red}Open Tesouraria Error: {yellow}\n\t{err}{bg}\n")
            return False

    def debt(self, debt: dict) -> bool:
        try:
            WebDriverWait(self.driver, 7)\
                        .until(expected_conditions\
                            .presence_of_element_located((By.ID, "f_data")))

            # Inserts document date
            self.driver.find_element_by_id("f_data").send_keys(debt["date"])
            
            # Inserts document type
            self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-7"]').click()
            doc = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen7_search"]')
            doc.click()
            doc.send_keys(debt["type"])
            doc.send_keys(Keys.RETURN)
            
            # Inserts document number
            doc  = self.driver.find_element(By.ID, "f_documento")
            doc.click()
            doc.send_keys(debt["num"])

            # Inserts document value
            doc  = self.driver.find_element(By.ID, "f_valor")
            doc.click()
            doc.send_keys(debt["value"])
            doc.send_keys(Keys.RETURN)

            # Inserts document expenditure (Tipo de Despesa)            
            doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen8_search"]')
            doc.click()
            doc.send_keys(debt["expenditure"])
            doc.send_keys(Keys.RETURN)

            # Inserts document cost center
            doc  = self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-9"]')
            doc.click()

            doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen9_search"]')
            doc.click()
            doc.send_keys(debt["cost-center"])
            doc.send_keys(Keys.RETURN)

            # Inserts document emitter
            self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-14"]').click()
            doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen14_search"]')
            doc.click()
            doc.send_keys(debt["emitter"])
            doc.send_keys(Keys.RETURN)
            sleep(2)
            doc.send_keys(Keys.RETURN)

            # Inserts document historic 1
            self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-10"]').click()
            doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen10_search"]')
            doc.click()
            doc.send_keys(debt["hist-1"])
            doc.send_keys(Keys.RETURN)

            # Inserts payment date
            doc = self.driver.find_element_by_id("f_datapagamento")
            doc.send_keys(debt["date"])

            # Inserts payment form
            self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-11"]').click()
            doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen11_search"]')
            doc.click()
            doc.send_keys(debt["payment-form"])
            doc.send_keys(Keys.RETURN)

            # Inserts payment form
            if debt["payment-form"] == "CHEQUE"\
                and debt["check-num"] is not None:
                self.driver.find_element_by_id("f_numerocheque").click()
                self.driver.find_element_by_id("f_numerocheque").send_keys(debt["check-num"])

            elif debt["payment-form"] == "DEBITO AUTOMATICO":
                self.driver.find_element_by_id("f_documento2").click()
                self.driver.find_element_by_id("f_documento2").send_keys(debt["doc-num"])

            # Inserts payment cost account
            self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-12"]').click()
            doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen12_search"]')
            doc.click()
            doc.send_keys(debt["cost-account"])
            doc.send_keys(Keys.RETURN)

            # Inserts document historic 2
            self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-13"]').click()
            doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen13_search"]')
            doc.click()
            doc.send_keys(debt["hist-2"])
            doc.send_keys(Keys.RETURN)
            
            return True

        except Exception as err:
            print(err)
            insert_execlog(f"{red}Debt Insertion Error: {yellow}\n\t{err}{bg}\n")
            return False
        
    def file_upload(self, file_path) -> bool:
        try:
            # self.driver.find_element(By.XPATH, file_upload_place).click()
            documento  = self.driver.find_element(By.ID, 'f_anexos')
            documento.send_keys(file_path)

            sleep(3)

            # if not WIN:
            #     pyautogui.write(file_path)
            #     sleep(2)
            #     enter()

            # else:
            #     # Windows implementation
            #     msg = "UPLOAD para Windows não foi implementado"
            #     insert_execlog(f"{red}File Upload Error: {yellow}\n\t{msg}{bg}\n")

            return True

        except Exception as err:
            insert_execlog(f"{red}File Upload Error: {yellow}\n\t{err}{bg}\n")
            return False

    def save_debt(self, debt: dict) -> bool:
        try:
            self.driver.find_element(By.XPATH, save_debt_btn).click()

            sleep(4)
            # modal ja existe documento com o mesmo numero
            modal_header = '/html/body/div[17]/div[1]/h3' 
            modal_btn_no_xpath = '/html/body/div[17]/div[3]/a[2]'

            modal_header_title = self.driver.find_element(By.XPATH, modal_header)
            if modal_header_title.size != 0 or modal_header_title.is_diplayed():
                self.driver.find_element(By.XPATH, modal_btn_no_xpath).click()
                
            if debt["payment-form"] == "CHEQUE":
                form_print_check_header = '/html/body/div[12]/div/div/h3'
                form_print_check_close = '/html/body/div[12]/div/div/a[1]' 
                sleep(4)
                pyautogui.press("tab")
                enter()

            sleep(3)
            confirm_modal = self.driver.find_element(By.XPATH, modal_header_success_confirm)
            if confirm_modal.size != 0 or confirm_modal.is_diplayed():
                confirm_modal.click()

            return True
        except NoSuchElementException as err:
            insert_execlog(f"{red}Save Debt Error: {yellow}\n\t{err}{bg}\n")
            return False

    def save_and_new_debt(self, debt: dict) -> bool:
        try:
            self.driver.find_element(By.XPATH, save_and_new_debt_btn).click()

            # modal ja existe documento com o mesmo numero
            sleep(4)
            modal_header = '/html/body/div[17]/div[1]/h3' 
            modal_btn_no_xpath = '/html/body/div[17]/div[3]/a[2]'

            modal_header_title = self.driver.find_element(By.XPATH, modal_header)
            if modal_header_title.size != 0 or modal_header_title.is_diplayed():
                self.driver.find_element(By.XPATH, modal_btn_no_xpath).click()
                
            if debt["payment-form"] == "CHEQUE":
                sleep(4)
                pyautogui.press("tab")
                enter()

            return True
        except NoSuchElementException as err:
            insert_execlog(f"{red}Save New Debt Error: {yellow}\n\t{err}{bg}\n")
            return False

    def new_debt(self) -> bool:
        try:
            self.driver.find_element_by_css_selector(new_debt_select_box).click()
            sleep(3)
            self.driver.find_element_by_link_text(new_debt_select_element).click()
            sleep(2)
            return True
        except Exception as err:
            insert_execlog(f"{red}New Debt Error: {yellow}\n\t{err}{bg}\n")
            return False

    def new_group_debt(self):
        self.driver.find_element(By.XPATH, new_group_debt_select_box).click()
        sleep(2)
        self.driver.find_element(By.XPATH, new_group_debt_select_element).click()

    def new_intern_transaction(self):
        self.driver.find_element(By.XPATH, new_intern_trans_select_box).click()
        sleep(2)
        self.driver.find_element(By.XPATH, new_intern_trans_select_element).click()

    def new_receive(self):
        self.driver.find_element(By.XPATH, new_receive_select_box).click()
        sleep(2)
        self.driver.find_element(By.XPATH, new_receive_select_element).click()

    
    def insert_debts(self, work_month_path:str, modelized_data: list) -> bool:
        pass
        
