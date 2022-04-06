from time import sleep
import pyautogui

from autom.strings import *
from utils.main import WIN, enter

from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
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
            sleep(4)
            self.driver.find_element(By.XPATH, open_select_month_date).click()
            sleep(2)
            pyautogui.write(month)
            enter(4)
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
            data_documento = self.driver.find_element_by_id("f_data")
            data_documento.send_keys(debt["date"])
            enter()

            # Inserts document type
            pyautogui.write(debt["type"])
            enter(2)
            sleep(2)

            # Inserts document number
            pyautogui.write(debt["num"])
            sleep(0.5)
            enter()
            sleep(2)

            # Inserts document value
            pyautogui.write(debt["value"])
            sleep(0.5)
            enter()
            sleep(1)

            # Inserts document expenditure (Tipo de Despesa)
            pyautogui.write(debt["expenditure"])
            sleep(3)
            enter(2)

            # Inserts document cost center
            pyautogui.write(debt["cost-center"])
            sleep(1)
            enter()

            # Inserts document emitter
            try:
                self.driver.find_element(By.XPATH, select_doc_emitter_opt1).click()
            except NoSuchElementException:
                self.driver.find_element(By.XPATH, select_doc_emitter_opt2).click()
            
            sleep(2)
            pyautogui.write(debt["emitter"])
            enter(3, 1)

            # Inserts document historic 1 
            pyautogui.write(debt["hist-1"])
            enter(3)

            # Inserts document payment date
            sleep(1)
            for i in range(3): 
                pyautogui.write(debt["date"][i])
                sleep(0.5)
            enter()

            # Inserts payment form
            if debt["payment-form"] == "CHEQUE"\
                and debt["check-num"] is not None:
                # Inserts payment form
                pyautogui.write(debt["payment-form"])
                sleep(2)
                enter(3)

                # Inserts check number
                sleep(1)
                pyautogui.write(debt["check-num"])
                enter(4)
                
                # Inserts document cost account
                pyautogui.write(debt["cost-account"])
                enter()

                # Inserts payment historic
                pyautogui.write(debt["hist-2"])
                enter()

            elif debt["payment-form"] == "DEBITO AUTOMATICO":
                pass
                # Inserts payment form
                pyautogui.write(debt["payment-form"])
                sleep(2)
                enter(2)

                # Inserts document number
                pyautogui.write(debt["doc-num"])
                sleep(0.5)
                enter()
                
                # Inserts document cost account
                pyautogui.write(debt["cost-account"])
                enter(2)

                # Inserts document historic 2
                pyautogui.write(debt["hist-2"])
                enter()

            else:
                sleep(1)
                pyautogui.write(debt["payment-form"])
                sleep(1)
                enter(2)

                # Inserts document cost account
                pyautogui.write(debt["cost-account"])
                enter(2)
            
                # Inserts payment historic
                pyautogui.write(debt["hist-2"])
                sleep(0.5)
                enter()
            
            return True

        except Exception as err:
            print("Debt exception: ", err)
            insert_execlog(f"{red}Debt Insertion Error: {yellow}\n\t{err}{bg}\n")
            return False
        
    def file_upload(self, file_path) -> bool:
        try:
            self.driver.find_element(By.XPATH, file_upload_place).click()
            sleep(3)

            if not WIN:
                pyautogui.write(file_path)
                sleep(2)
                enter()

            else:
                # Windows implementation
                pass

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
        
