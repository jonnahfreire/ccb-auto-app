from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from routes import Siga

class Selenium:
    # Set path Selenium
    CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    s = Service(CHROMEDRIVER_PATH)
    WINDOW_SIZE = "1920,1080"
    # Options
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # no pop window
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument('--no-sandbox')

    def __init__(self, target: str) -> None:
        self.target = target
        self.driver = webdriver.Chrome(service=self.s, options=self.chrome_options)

    def set_driver_path(self, path):
        pass

    def start(self):
        self.driver.get(self.target)

    def close(self):
        self.driver.close()
    
    def get_driver(self):
        return self.driver




if __name__ == "__main__":
    target = "https://appl2.ccbsiga.congregacao.org.br/index.aspx"
    selenium = Selenium(target)
    selenium.start()

    siga = Siga(selenium.get_driver())

    sleep(2)
    siga.login("jonas.freire.3", "@nopass1726")
    sleep(5)
    selenium.close()
    # siga.open_tesouraria()
    sleep(4)
    # siga.new_debt()
    sleep(5)





