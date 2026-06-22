from selenium.webdriver.common.by import By
from utils.helpers import wait_for_element, wait_for_clickable


class LoginPage:
    URL = "/web/index.php/auth/login"

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MSG = (By.CSS_SELECTOR, ".oxd-alert-content-text")

    def __init__(self, driver):
        self.driver = driver

    def open(self, base_url):
        self.driver.get(f"{base_url}{self.URL}")

    def enter_username(self, username):
        wait_for_element(self.driver, self.USERNAME).send_keys(username)

    def enter_password(self, password):
        wait_for_element(self.driver, self.PASSWORD).send_keys(password)

    def click_login(self):
        wait_for_clickable(self.driver, self.LOGIN_BTN).click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        return wait_for_element(self.driver, self.ERROR_MSG).text
