from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


from app.config.globals import selenium_brw_size
from app.config.settings import get_chromedriver_path

class Selenium:
    chrome_options = Options()
    chrome_options.add_argument("--window-size=%s" % selenium_brw_size)
    

    def __init__(self, target: str, show_browser_window: bool = False) -> None:
        if not show_browser_window:
            self.chrome_options.add_argument("--headless") # no pop window
            self.chrome_options.add_argument('--no-sandbox')
            
        self.target = target
        self.driver = None

    def start(self):
        self.driver = webdriver.Chrome(
                        service=Service(get_chromedriver_path()), 
                        options=self.chrome_options)
        
        self.driver.get(self.target)

    def close(self) -> None:
        self.driver.close()
    
    def get_driver(self) -> webdriver:
        return self.driver
    
    def refresh(self):
        self.driver.refresh()
        