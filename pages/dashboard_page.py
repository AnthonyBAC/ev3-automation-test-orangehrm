from selenium.webdriver.common.by import By
from utils.helpers import wait_for_element


class DashboardPage:
    HEADER = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")

    def __init__(self, driver):
        self.driver = driver

    def is_displayed(self):
        header = wait_for_element(self.driver, self.HEADER)
        return header.is_displayed()

    def get_header_text(self):
        return wait_for_element(self.driver, self.HEADER).text
