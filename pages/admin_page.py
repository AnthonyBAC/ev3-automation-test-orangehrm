from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import wait_for_element, wait_for_clickable


class AdminPage:
    SEARCH_USERNAME = (By.XPATH, "//label[text()='Username']/following::input[1]")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
    EDIT_ICON = (By.CSS_SELECTOR, "i.oxd-icon.bi-pencil-fill")
    USER_ROLE_DROPDOWN = (By.XPATH, "//label[text()='User Role']/following::div[contains(@class,'oxd-select-text-input')][1]")
    STATUS_DROPDOWN = (By.XPATH, "//label[text()='Status']/following::div[contains(@class,'oxd-select-text-input')][1]")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    SUCCESS_TOAST = (By.CSS_SELECTOR, ".oxd-toast-content--success")
    ERROR_MESSAGES = (By.CSS_SELECTOR, ".oxd-input-field-error-message")
    USERNAME_INPUT = (By.XPATH, "//label[text()='Username']/following::input[1]")

    def __init__(self, driver):
        self.driver = driver

    def search_user(self, username):
        self._wait_for_loader()
        wait_for_element(self.driver, self.SEARCH_USERNAME)
        self._wait_for_loader()
        search_input = wait_for_clickable(self.driver, self.SEARCH_USERNAME)
        search_input.click()
        search_input.send_keys(Keys.CONTROL + "a")
        search_input.send_keys(Keys.DELETE)
        search_input.send_keys(username)
        self._wait_for_loader()
        wait_for_clickable(self.driver, self.SEARCH_BUTTON).click()

    def _wait_for_loader(self, timeout=15):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-form-loader"))
            )
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".oxd-form-loader"))
            )
        except Exception:
            pass

    def click_edit_first_result(self):
        self._wait_for_loader()
        edit = wait_for_clickable(self.driver, self.EDIT_ICON)
        try:
            edit.click()
        except Exception:
            edit = wait_for_clickable(self.driver, self.EDIT_ICON)
            edit.click()
        self._wait_for_loader()

    def get_user_role(self, timeout=10):
        def _role_has_value(driver):
            text = driver.find_element(*self.USER_ROLE_DROPDOWN).text
            return text and text != "-- Select --"

        WebDriverWait(self.driver, timeout).until(_role_has_value)
        return self.driver.find_element(*self.USER_ROLE_DROPDOWN).text

    def set_user_role(self, role):
        self._select_dropdown("User Role", role)

    def _select_dropdown(self, label, value):
        self._wait_for_loader()
        dropdown = wait_for_clickable(self.driver, (By.XPATH, f"//label[text()='{label}']/following::div[contains(@class,'oxd-select-text-input')][1]"))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
        dropdown.click()
        option = wait_for_clickable(self.driver, (By.XPATH, f"//div[@role='option']//span[text()='{value}']"))
        option.click()

    def clear_required_fields(self):
        username = wait_for_element(self.driver, self.USERNAME_INPUT)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", username)
        self.driver.execute_script(
            """
            var el = arguments[0];
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(el, '');
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            username,
        )

    def click_save(self):
        save = wait_for_clickable(self.driver, self.SAVE_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save)
        self.driver.execute_script("arguments[0].click();", save)

    def get_success_toast_text(self, timeout=10):
        try:
            return wait_for_element(self.driver, self.SUCCESS_TOAST, timeout).text
        except Exception:
            return ""

    def get_error_messages(self, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGES)
            )
            elements = self.driver.find_elements(*self.ERROR_MESSAGES)
            return [el.text for el in elements if el.text.strip()]
        except Exception:
            return []

    def is_on_admin_module(self):
        try:
            header = wait_for_element(self.driver, (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6"))
            return header.text == "Admin"
        except Exception:
            return False

    def get_role_from_grid(self, username):
        self._wait_for_loader()
        self.search_user(username)
        self._wait_for_loader()
        try:
            row_locator = (
                By.XPATH,
                f"//div[contains(@class,'oxd-table-row') and .//div[contains(@class,'oxd-table-cell')][2][text()='{username}']]"
            )
            row = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(row_locator))
            cell = row.find_element(By.XPATH, ".//div[contains(@class,'oxd-table-cell')][3]")
            return cell.text
        except Exception:
            return ""

    def edit_and_set_role(self, username, role):
        self._wait_for_loader()
        self.search_user(username)
        self.click_edit_first_result()
        self.set_user_role(role)
        self.click_save()
        self._wait_for_loader()
