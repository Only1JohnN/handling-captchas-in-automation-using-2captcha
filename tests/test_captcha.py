import pytest
from selenium import webdriver
from pages.captcha_page import CaptchaPage
from time import sleep

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
    
def test_solve_captcha(driver):
    page_url = "https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox.php"
    site_key = "6LfW6wATAAAAAHLqO2pb8bDBahxlMxNdo9g947u9"
    api_key = "6d4022c6d7d0372ad1df7c786dd814ce"
    
    #Initialize the page object
    captcha_page = CaptchaPage(driver, api_key, site_key, page_url)
    
    #Open the CAPTCHA page
    driver.get(page_url)
    
    #Fill the input fields
    captcha_page.fill_input_fields("Adeniyi", "John")
    
    #Solve the CAPTCHA
    captcha_solution = captcha_page.solve_captcha()
    sleep(2)
    
    #Submit the form
    captcha_page.submit_form(captcha_solution)
    sleep(2)
    
    #Verify that the submission was succesful
    assert captcha_page.is_submission_successful(), "Form submission failed."
    sleep(2)