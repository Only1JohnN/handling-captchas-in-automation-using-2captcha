#pages/captcha_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import requests
from time import sleep


class CaptchaPage(BasePage):
    
    # Locators for elements on the CAPTCHA page
    INPUT_A = (By.NAME, "ex-a")
    INPUT_B = (By.NAME, "ex-b")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CAPTCHA_FRAME = (By.CSS_SELECTOR, "iframe[src*='recaptcha']")
    

    def __init__(self, driver, api_key, site_key, page_url):
        super().__init__(driver)
        self.api_key = api_key
        self.site_key = site_key
        self.page_url = page_url


    # Fill the input fields
    def fill_input_fields(self, a_value, b_value):
        self.enter_text(self.INPUT_A, a_value)
        self.enter_text(self.INPUT_B, b_value)


    # Solve the CAPTCHA using 2Captcha
    def solve_captcha(self):
        captcha_url = 'http://2captcha.com/in.php'
        captcha_response_url = 'http://2captcha.com/res.php'

        # Step 1: Submit CAPTCHA solving request to 2Captcha
        payload = {
            'key': self.api_key,
            'method': 'userrecaptcha',
            'googlekey': self.site_key,
            'pageurl': self.page_url,
            'json': 1
        }
        
        print("Solving CAPTCHA...")
        response = requests.post(captcha_url, data=payload)
        captcha_id = response.json().get('request')

        # Step 2: Poll for CAPTCHA solution
        if response.json().get('status') == 1:
            sleep(20)  # Wait for CAPTCHA to be solved by 2Captcha
            for _ in range(20):
                check_payload = {
                    'key': self.api_key,
                    'action': 'get',
                    'id': captcha_id,
                    'json': 1
                }
                result = requests.post(captcha_response_url, data=check_payload)
                if result.json().get('status') == 1:
                    return result.json().get('request')  # CAPTCHA solved
                sleep(5)  # Wait and retry every 5secs
        else:
            raise Exception(f"Error from 2Captcha: {response.json().get('request')}")
        

    
    # Submit the form
    def submit_form(self, captcha_solution):
        # Inject CAPTCHA response
        self.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{captcha_solution}';")
        
        # Click submit button
        self.click(self.SUBMIT_BUTTON)

    # Validate success
    def is_submission_successful(self):
        return "Success" in self.driver.page_source
    
    
