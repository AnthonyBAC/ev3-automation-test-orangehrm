from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unittest import TestCase


# Wait helpers
def wait_for_element(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )

def wait_for_clickable(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


# Assertion helpers
_tc = TestCase()

def assert_true(condition, message=None):
    _tc.assertTrue(condition, message)

def assert_equal(first, second, message=None):
    _tc.assertEqual(first, second, message)
