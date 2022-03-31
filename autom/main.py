from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
WINDOW_SIZE = "1920,1080"

# chrome_options.add_argument("--headless") # no pop window
# chrome_options.add_argument('--no-sandbox')

class Selenium:
    chrome_options = Options()
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

    def __init__(self, target: str) -> None:
        self.target = target
        self.driver = None

    def set_driver_path(self, path):
        pass

    def start(self):
        self.driver = webdriver.Chrome(
            service=Service(CHROMEDRIVER_PATH), 
            options=self.chrome_options)
        self.driver.get(self.target)

    def close(self):
        self.driver.close()
    
    def get_driver(self):
        return self.driver
        




if __name__ == "__main__":
    pass





