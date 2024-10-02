#pages/base_page.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        
        
    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def click(self, locator):
        self.find_element(locator).click()
        
    def enter_text(self, locator, text):
        self.find_element(locator).clear()
        self.find_element(locator).send_keys(text)
        
    def execute_script(self, script, *args):
        self.driver.execute_script(script, *args)