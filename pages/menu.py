from selenium.webdriver.common.by import By
from utils.helpers import wait_for_clickable


class Menu:
    def __init__(self, driver):
        self.driver = driver

    def _menu_item(self, name):
        return (By.XPATH, f"//span[contains(@class,'oxd-main-menu-item--name') and text()='{name}']")

    def navigate_to(self, name):
        wait_for_clickable(self.driver, self._menu_item(name)).click()
