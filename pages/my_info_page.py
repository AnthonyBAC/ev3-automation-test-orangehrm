from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import wait_for_element, wait_for_clickable


class MyInfoPage:
    FIRST_NAME = (By.NAME, "firstName")
    MIDDLE_NAME = (By.NAME, "middleName")
    LAST_NAME = (By.NAME, "lastName")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    SUCCESS_TOAST = (By.CSS_SELECTOR, ".oxd-toast-content--success")
    ERROR_MESSAGES = (By.CSS_SELECTOR, ".oxd-input-field-error-message")

    def __init__(self, driver):
        self.driver = driver

    def get_first_name(self):
        return wait_for_element(self.driver, self.FIRST_NAME).get_attribute("value")

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

    def _clear_field(self, locator):
        self._wait_for_loader()
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

    def update_middle_name(self, middle_name):
        self._clear_field(self.MIDDLE_NAME)
        wait_for_element(self.driver, self.MIDDLE_NAME).send_keys(middle_name)

    def click_save(self):
        wait_for_clickable(self.driver, self.SAVE_BUTTON).click()

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

    def is_on_my_info(self):
        try:
            self._wait_for_loader()
            header = wait_for_element(self.driver, (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6"))
            return header.text == "PIM" and "viewPersonalDetails" in self.driver.current_url
        except Exception:
            return False
