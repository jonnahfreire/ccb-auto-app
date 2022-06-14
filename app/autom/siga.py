from time import sleep

from app.autom.strings import *
from app.config.globals import form_ids

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from selenium.common.exceptions import NoSuchElementException, TimeoutException

from app.execlogs.logs import *
from app.execlogs.notifications import *
from app.cli.colors import *


class Siga:

    def __init__(self, driver) -> None:
        self.driver = driver
        self.notification: Notification = Notification()

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
            sleep(1)
            self.driver.find_element_by_link_text(open_month_date_options).click()
            sleep(1.5)
            self.driver.find_element(By.XPATH, open_select_month_date).click()
            sleep(2)
            input_month = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen10_search"]')
            input_month.send_keys(month)
            input_month.send_keys(Keys.RETURN)
            sleep(0.5)

            forms = self.driver.find_elements(By.TAG_NAME, 'form')
            ids = [form.get_attribute("id") for form in forms]

            btn_save_id = [_id for _id in ids if _id not in form_ids][0]
            btn_save_xpath = f'//*[@id="{btn_save_id}"]/div[2]/button'

            self.driver.find_element(By.XPATH, btn_save_xpath).click()
            return True

        except NoSuchElementException as ex:
            insert_execlog(f"{red}ChangeWorkMonth Exception: {yellow}\n\t{ex}{bg}\n")
            sleep(5)
            return False

    def open_tesouraria(self) -> bool:
        try:
            self.driver.find_element(By.XPATH, menu_tesouraria).click()
            sleep(2)
            self.driver.find_element(By.XPATH, caixa_bancos).click()

            return True
        except Exception as ex:
            insert_execlog(f"{red}Open Tesouraria Exception: {yellow}\n\t{ex}{bg}\n")
            return False

    def debt(self, debt: dict) -> bool:
        try:
            WebDriverWait(self.driver, 7)\
                .until(expected_conditions\
                    .presence_of_element_located((By.ID, "f_data")))

            # Inserts document date
            self.driver.find_element_by_id("f_data").send_keys(debt["date"])
            sleep(1)
            
            # Inserts document type
            try:
                self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-7"]').click()
                sleep(1)
                doc = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen7_search"]')
                doc.click()
                sleep(0.5)
                doc.send_keys(debt["type"])
                doc.send_keys(Keys.RETURN)
            except Exception as ex:
                print("EXCEPTION INSERTING DOC TYPE: ", ex)

            try:
                # Inserts document number
                sleep(1)
                doc  = self.driver.find_element(By.ID, "f_documento")
                doc.click()
                sleep(0.5)
                doc.send_keys(debt["num"])
            except NoSuchElementException as ex:
                print("EXCEPTION INSERTING DOC NUM: ", ex)
            
            try:
                # Inserts document value
                sleep(1)
                doc  = self.driver.find_element(By.ID, "f_valor")
                doc.click()
                sleep(0.5)
                doc.send_keys(debt["value"])
                doc.send_keys(Keys.RETURN)
            except NoSuchElementException as ex:
                print("EXCEPTION INSERTING DOC VALUE: ", ex)

            try:
                # Inserts document expenditure (Tipo de Despesa)  
                sleep(1)          
                doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen8_search"]')
                doc.click()
                sleep(0.5)
                doc.send_keys(debt["expenditure"])
                doc.send_keys(Keys.RETURN)
            except NoSuchElementException as ex:
                print("EXCEPTION INSERTING DOC EXPENDITURE: ", ex)

            try:
                # Inserts document cost center
                sleep(1)
                self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-9"]').click()
                sleep(0.5)
                doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen9_search"]')
                doc.click()
                sleep(0.5)
                doc.send_keys(debt["cost-center"])
                doc.send_keys(Keys.RETURN)
            except NoSuchElementException as ex:
                print("EXCEPTION INSERTING DOC COST CENTER: ", ex)

            try:
                # Inserts document emitter
                sleep(1)
                self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-14"]').click()
                sleep(0.5)
                doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen14_search"]')
                doc.click()
                sleep(0.5)
                doc.send_keys(debt["emitter"])
                doc.send_keys(Keys.RETURN)
                sleep(2)
                doc.send_keys(Keys.RETURN)
            except NoSuchElementException as ex:
                print("EXCEPTION INSERTING DOC EMITTER: ", ex)

            try:
                # Inserts document historic 1
                sleep(1)
                self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-10"]').click()
                sleep(0.5)
                doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen10_search"]')
                doc.click()
                sleep(0.5)
                doc.send_keys(debt["hist-1"])
                doc.send_keys(Keys.RETURN)
            except NoSuchElementException as ex:
                print("EXCEPTION INSERTING DOC HIST1: ", ex)

            try:
                # Inserts payment date
                sleep(2)
                doc = self.driver.find_element_by_id("f_datapagamento")
                sleep(1)
                doc.send_keys(debt["date"])
            except NoSuchElementException as ex:
                print("EXCEPTION INSERTING DOC PAYMENT DATE: ", ex)

            try:
                # Inserts payment form
                sleep(1)
                self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-11"]').click()
                sleep(0.5)
                doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen11_search"]')
                doc.click()
                sleep(0.5)
                doc.send_keys(debt["payment-form"])
                doc.send_keys(Keys.RETURN)
            except NoSuchElementException as ex:
                print("EXCEPTION INSERTING DOC PAYMENT FORM: ", ex)


            # Inserts payment form
            sleep(1)
            if debt["payment-form"] == "CHEQUE"\
                and debt["check-num"] is not None:
                try:
                    self.driver.find_element_by_id("f_numerocheque").click()
                    sleep(0.5)
                    self.driver.find_element_by_id("f_numerocheque").send_keys(debt["check-num"])
                except NoSuchElementException as ex:
                    print("EXCEPTION INSERTING DOC PAYMENT CHEQUE: ", ex)

            elif debt["payment-form"] == "DEBITO AUTOMATICO":
                try:
                    self.driver.find_element_by_id("f_documento2").click()
                    sleep(0.5)
                    self.driver.find_element_by_id("f_documento2").send_keys(debt["doc-num"])
                except NoSuchElementException as ex:
                    print("EXCEPTION INSERTING DOC PAYMENT DEB AT: ", ex)

            try:
                # Inserts payment cost account
                sleep(1)
                self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-12"]').click()
                sleep(0.5)
                doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen12_search"]')
                doc.click()
                sleep(0.5)
                doc.send_keys(debt["cost-account"])
                doc.send_keys(Keys.RETURN)
            except NoSuchElementException as ex:
                print("EXCEPTION INSERTING DOC COST ACCOUNT: ", ex)

            try:
                # Inserts document historic 2
                sleep(1)
                self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-13"]').click()
                sleep(0.5)
                doc  = self.driver.find_element(By.XPATH, '//*[@id="s2id_autogen13_search"]')
                doc.click()
                sleep(0.5)
                doc.send_keys(debt["hist-2"])
                doc.send_keys(Keys.RETURN)
                sleep(1)
            except NoSuchElementException as ex:
                print("EXCEPTION INSERTING DOC HIST2: ", ex)
            
            return True

        except Exception as ex:
            insert_execlog(f"{red}Debt Insertion Exception: {yellow}\n\t{ex}{bg}\n[Trying again..]\n")
        
    def file_upload(self, file_path: str) -> bool:
        try:
            documento  = self.driver.find_element(By.ID, 'f_anexos')
            documento.send_keys(file_path)
            sleep(3)

            return True
        except Exception as ex:
            insert_execlog(f"{red}File Upload Exception: {yellow}\n\t{ex}{bg}\n")
            return False

    def save(self, item: dict, save_btn: str = None) -> bool:
        document_already_exists: bool = False
        try:
            if item["insert-type"] == "MOVINT":
                save_btn = btn_save_intern_transf

            if save_btn is not None:
                self.driver.find_element(By.XPATH, save_btn).click()
            else:
                self.driver.find_element(By.XPATH, save_debt_btn).click()

            sleep(4)
            # modal ja existe documento com o mesmo numero
            try:
                if not item["insert-type"] == "MOVINT":
                    modal_header_title = self.driver.find_element(By.XPATH, modal_header)
                    if modal_header_title.size != 0 or modal_header_title.is_diplayed():
                        document_already_exists = True
                        self.driver.find_element(By.XPATH, modal_btn_no_xpath).click()

                    return False
            
            except NoSuchElementException as ex:
                message = "Falha ao fechar modal de 'Documento já existe'"
                if document_already_exists:
                    message += f"\n\t'Documento com o mesmo número já existe'"
                insert_execlog(f"{red}Save Debt Exception: {yellow}\n\t{message}\n\t{ex.msg}{bg}\n")
                
            if item["insert-type"] == "MOVINT" or item["payment-form"] == "CHEQUE":
                message = "Falha ao fechar modal de imprimir cópia de cheque"
                close = '/html/body/div[18]/div/div/a[1]'
                try:
                    try:
                        if item["insert-type"] == "MOVINT":
                            close = '/html/body/div[13]/div/div/a[1]'

                        WebDriverWait(self.driver, 4)\
                            .until(expected_conditions\
                                .presence_of_element_located((By.XPATH, close)))

                        self.driver.find_element(By.XPATH, close).click()
                            
                        return True
    
                    except TimeoutException as ex:
                        if document_already_exists:
                            message += f"\n\t'Documento com o mesmo número já existe'"
                        insert_execlog(f"{red}Save Debt Exception: {yellow}\n\t{message}\n\t{ex.msg}{bg}\n")

                        if not item["insert-type"] == "MOVINT":
                            return False
                        
                except NoSuchElementException as ex:
                    insert_execlog(f"{red}Save Debt Exception: {yellow}\n\t{message}\n\t{ex.msg}{bg}\n")

            if item["insert-type"] == "MOVINT":
                return True

            sleep(3)
            message = "Falha ao confirmar modal 'lançamento com sucesso'"
            try:
                try:
                    WebDriverWait(self.driver, 4)\
                        .until(expected_conditions\
                            .presence_of_element_located((By.XPATH, modal_header_success_confirm)))

                except TimeoutException as ex:
                    insert_execlog(f"{red}Save Debt Exception: {yellow}\n\t{message}\n\t{ex.msg}{bg}\n")

                confirm_modal = self.driver.find_element(By.XPATH, modal_header_success_confirm)
                if confirm_modal.size != 0 or confirm_modal.is_diplayed():
                    confirm_modal.click()

                    return True

            except NoSuchElementException as ex:
                insert_execlog(f"{red}Save Debt Exception: {yellow}\n\t{message}\n\t{ex.msg}{bg}\n")

            return True

        except NoSuchElementException as ex:
            insert_execlog(f"{red}Save Debt Exception: {yellow}\n\t{ex}{bg}\n")
            return False
        except Exception as ex:
            insert_execlog(f"{red}Save Debt Exception: {yellow}\n\t{ex}{bg}\n")
            return False

    def save_and_new_debt(self, debt: dict) -> bool:
        return self.save_debt(debt, save_and_new_debt_btn)  
        
    def new_debt(self) -> bool:
        try:
            try:
                WebDriverWait(self.driver, 7)\
                            .until(expected_conditions\
                                .presence_of_element_located((By.XPATH, new_debt_select_box)))
            except TimeoutException as ex:
                insert_execlog(f"{red}New Debt Exception: {yellow}\n\t{ex}{bg}\n")

            self.driver.find_element(By.XPATH, new_debt_select_box).click()
            sleep(3)
            self.driver.find_element_by_link_text(new_debt_select_element).click()
            sleep(5)
            return True
        except Exception as err:
            insert_execlog(f"{red}New Debt Error: {yellow}\n\t{err}{bg}\n")
            return False

    def new_group_debt(self):
        self.driver.find_element(By.XPATH, new_group_debt_select_box).click()
        sleep(2)
        self.driver.find_element(By.XPATH, new_group_debt_select_element).click()

    def new_intern_transaction(self, item: list) -> bool:
        try:
            try:
                # WebDriverWait(self.driver, 7)\
                #     .until(expected_conditions\
                #         .presence_of_element_located((By.XPATH, new_intern_trans_select_box)))
                self.driver.find_element(By.XPATH, new_intern_trans_select_box).click()
                sleep(2)
                self.driver.find_element(By.XPATH, new_intern_trans_select_element).click()

            except TimeoutException as ex:
                insert_execlog(f"{red}New Movint Exception: {yellow}\n\t{ex}{bg}\n")

            date_picker = '//*[@id="f_data"]'

            transform_drop = '//*[@id="select2-chosen-7"]'
            transform_input = '//*[@id="s2id_autogen7_search"]' # forma de transferencia
            num_doc_input = '//*[@id="f_documento"]'
            value = '//*[@id="f_valor"]'
            receiver = '//*[@id="f_nomefavorecido"]' #favorecido
            orig_account_drop = '//*[@id="select2-chosen-8"]'
            orig_account_input = '//*[@id="s2id_autogen8_search"]'
            dest_account_drop = '//*[@id="select2-chosen-10"]'
            dest_account_input = '//*[@id="s2id_autogen10_search"]'
            hist = '//*[@id="select2-chosen-9"]'
            hist_input = '//*[@id="s2id_autogen9_search"]'
            complement = '//*[@id="f_complemento"]'

            sleep(5)
            date_picker = self.driver.find_element(By.XPATH, date_picker).send_keys(item["date"])

            sleep(2)
            self.driver.find_element(By.XPATH, transform_drop).click()
            transform_input = self.driver.find_element(By.XPATH, transform_input)
            transform_input.click()
            sleep(0.5)
            transform_input.send_keys(item["transform"])
            transform_input.send_keys(Keys.RETURN)

            sleep(2)
            self.driver.find_element(By.XPATH, num_doc_input).send_keys(item["doc-num"])

            sleep(2)
            value = self.driver.find_element(By.XPATH, value)
            value.click()
            sleep(0.5)
            value.send_keys(item["value"])
            
            sleep(2)
            if item["receiver"] is not None:
                receiver = self.driver.find_element(By.XPATH, receiver)
                receiver.click()
                sleep(0.5)
                receiver.send_keys(item["receiver"])#"Congregação Cristã no Brasil"

            sleep(2)
            self.driver.find_element(By.XPATH, orig_account_drop).click()
            sleep(0.5)
            orig_account_input = self.driver.find_element(By.XPATH, orig_account_input)
            orig_account_input.send_keys(item["orig-account"])
            orig_account_input.send_keys(Keys.RETURN)
            
            sleep(2)
            self.driver.find_element(By.XPATH, dest_account_drop).click()
            sleep(0.5)
            dest_account_input = self.driver.find_element(By.XPATH, dest_account_input)
            dest_account_input.send_keys(item["dest-account"])
            dest_account_input.send_keys(Keys.RETURN)

            sleep(2)
            self.driver.find_element(By.XPATH, hist).click()
            sleep(0.5)
            hist_input = self.driver.find_element(By.XPATH, hist_input)
            hist_input.send_keys(item["hist"])
            hist_input.send_keys(Keys.RETURN)

            if item["complement"] is not None:
                sleep(2)
                complement = self.driver.find_element(By.XPATH, complement)
                complement.click()
                sleep(0.5)
                complement.send_keys(item["complement"])#"SUPRIMENTO DE CAIXA"
            
            # sleep(2)
            # self.driver.find_element(By.ID, file_upload_input).send_keys(item[])
            
            sleep(2)
            return True
        except NoSuchElementException as ex:
            insert_execlog(f"{red}New Movint Exception: {yellow}\n\t{ex}{bg}\n")
        
        except Exception as ex:
            insert_execlog(f"{red}New Movint Exception: {yellow}\n\t{ex}{bg}\n")

    def new_receive(self):
        self.driver.find_element(By.XPATH, new_receive_select_box).click()
        sleep(2)
        self.driver.find_element(By.XPATH, new_receive_select_element).click()

    
    def insert_debts(self, work_month_path:str, modelized_data: list) -> bool:
        pass
        
