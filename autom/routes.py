from time import sleep
import pyautogui

from autom.paths import *
from selenium.webdriver.common.by import By


class Siga:

    def __init__(self, driver) -> None:
        self.driver = driver

    def login(self, user, passw):
        user_input_user = self.driver.find_element(By.XPATH, input_user)
        user_input_user.click()
        user_input_user.send_keys(user)

        user_input_pass = self.driver.find_element(By.XPATH, input_pass)
        user_input_pass.click()
        user_input_pass.send_keys(passw)

        login_btn = self.driver.find_element(By.XPATH, login_confirm)
        login_btn.click()

    def change_work_month_date(self, month: str):
        self.driver.find_element(By.XPATH, work_month_date_select).click()
        sleep(1)
        self.driver.find_element(By.XPATH, open_month_date_options).click()
        sleep(4)
        self.driver.find_element(By.XPATH, open_select_month_date).click()
        sleep(2)
        pyautogui.write(month)
        for _ in range(4): pyautogui.press("enter")


    def open_tesouraria(self):
        self.driver.find_element(By.XPATH, menu_tesouraria).click()
        sleep(2)
        self.driver.find_element(By.XPATH, caixa_bancos).click()
        
    def debt_3026(self, debt):
        for i in range(3): pyautogui.write(debt["date"][i])
        pyautogui.press("enter")
        pyautogui.write(debt["type"])
        for _ in range(2): pyautogui.press("enter")
        pyautogui.write(debt["num"])
        pyautogui.press("enter")
        pyautogui.write(debt["value"])
        pyautogui.press("enter")
        pyautogui.write(debt["expenditure"])

        sleep(5)
        for _ in range(2): pyautogui.press("enter")
        pyautogui.write(debt["cost-center"])
        pyautogui.press("enter")
        self.driver.find_element(By.XPATH, '//*[@id="select2-chosen-14"]').click()
        sleep(2)
        pyautogui.write(debt["emitter"])
        for _ in range(3): 
            sleep(2)
            pyautogui.press("enter")
        pyautogui.write(debt["hist-1"])
        for _ in range(3): pyautogui.press("enter")
        
        for i in range(3): 
            sleep(0.3)
            pyautogui.write(debt["date"][i])

        pyautogui.press("enter")
        sleep(2)
        pyautogui.write(debt["bill-form"])
        sleep(1)
        pyautogui.press("enter")
        sleep(2)
        pyautogui.press("enter")
        pyautogui.write(debt["cost-account"])
        sleep(2)
        pyautogui.press("enter")
        sleep(2)
        pyautogui.press("enter")
        pyautogui.write(debt["hist-2"])
        sleep(2)
        pyautogui.press("enter")
        sleep(2)
        

    def file_upload(self, file_path):
        self.driver.find_element(By.XPATH, '//*[@id="tabAnexoAnexar"]/div/label').click()
        pyautogui.write(file_path)
        pyautogui.press("enter")

    def save_debt(self):
        self.driver.find_element(By.XPATH, '//*[@id="f_main"]/div[11]/button[1]').click()

    def new_debt(self):
        self.driver.find_element(By.XPATH, new_debt_select_box).click()
        sleep(2)
        self.driver.find_element(By.XPATH, new_debt_select_element).click()
        sleep(2)

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
