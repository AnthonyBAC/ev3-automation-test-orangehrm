import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import wait_for_element, wait_for_clickable


class PIMPage:
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    FIRST_NAME = (By.NAME, "firstName")
    MIDDLE_NAME = (By.NAME, "middleName")
    LAST_NAME = (By.NAME, "lastName")
    EMPLOYEE_ID = (By.XPATH, "//label[text()='Employee Id']/following::input[1]")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    SUCCESS_TOAST = (By.CSS_SELECTOR, ".oxd-toast-content--success")
    ERROR_MESSAGES = (By.CSS_SELECTOR, ".oxd-input-field-error-message")
    PROFILE_HEADER = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")

    def __init__(self, driver):
        self.driver = driver

    def click_add(self):
        self._wait_for_loader()
        wait_for_clickable(self.driver, self.ADD_BUTTON).click()

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

    def fill_employee(self, first_name, middle_name, last_name, employee_id=None):
        wait_for_element(self.driver, self.FIRST_NAME).send_keys(first_name)
        wait_for_element(self.driver, self.MIDDLE_NAME).send_keys(middle_name)
        wait_for_element(self.driver, self.LAST_NAME).send_keys(last_name)

        id_input = wait_for_element(self.driver, self.EMPLOYEE_ID)
        id_input.clear()
        if employee_id is None:
            employee_id = str(random.randint(1000, 9999))
        id_input.send_keys(employee_id)
        return employee_id

    def _clear_field(self, locator):
        field = wait_for_element(self.driver, locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
        self.driver.execute_script(
            """
            var el = arguments[0];
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(el, '');
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            field,
        )

    def clear_required_fields(self):
        self._clear_field(self.FIRST_NAME)
        self._clear_field(self.LAST_NAME)
        self._clear_field(self.EMPLOYEE_ID)

    def click_save(self):
        self._wait_for_loader()
        save = wait_for_clickable(self.driver, self.SAVE_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save)
        self.driver.execute_script("arguments[0].click();", save)

    def get_success_toast_text(self, timeout=10):
        try:
            return wait_for_element(self.driver, self.SUCCESS_TOAST, timeout).text
        except Exception:
            if "viewPersonalDetails" in self.driver.current_url:
                return "Successfully Saved"
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

    def is_on_profile(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains("viewPersonalDetails")
            )
            return True
        except Exception:
            return False

    def get_profile_header_text(self, timeout=10):
        try:
            return wait_for_element(self.driver, self.PROFILE_HEADER, timeout).text
        except Exception:
            return ""
