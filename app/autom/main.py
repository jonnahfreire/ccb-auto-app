from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


from app.config.globals import chrome_driver_path, selenium_brw_size


class Selenium:
    chrome_options = Options()
    chrome_options.add_argument("--window-size=%s" % selenium_brw_size)
    

    def __init__(self, target: str, no_window: bool = False) -> None:
        if no_window:
            self.chrome_options.add_argument("--headless") # no pop window
            self.chrome_options.add_argument('--no-sandbox')
            
        self.target = target
        self.driver = None

    def start(self):
        self.driver = webdriver.Chrome(
                        service=Service(chrome_driver_path), 
                        options=self.chrome_options)
        
        self.driver.get(self.target)

    def close(self) -> None:
        self.driver.close()
    
    def get_driver(self) -> webdriver:
        return self.driver
    
    def refresh(self):
        self.driver.refresh()
        




if __name__ == "__main__":
    pass





