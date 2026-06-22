from behave import given, when, then

from pages.login_page import LoginPage
from pages.menu import Menu
from utils.helpers import assert_true
from utils.config import BASE_URL, USERNAME, PASSWORD


@given('el usuario "Admin" ha iniciado sesión')
def step_admin_logged_in(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.open(BASE_URL)
    context.login_page.login(USERNAME, PASSWORD)


@when('navega al módulo "{module}"')
def step_navigate_to_module(context, module):
    menu = Menu(context.driver)
    menu.navigate_to(module)
    # Esperar a que el loader del módulo desaparezca (si existe)
    try:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        WebDriverWait(context.driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-form-loader"))
        )
        WebDriverWait(context.driver, 15).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".oxd-form-loader"))
        )
    except Exception:
        pass


@then('aparece el mensaje "{message}"')
def step_verify_toast(context, message):
    toast_text = ""
    if hasattr(context, "pim_page"):
        toast_text = context.pim_page.get_success_toast_text()
    elif hasattr(context, "admin_page"):
        toast_text = context.admin_page.get_success_toast_text()
    elif hasattr(context, "my_info_page"):
        toast_text = context.my_info_page.get_success_toast_text()

    assert_true(message in toast_text, f"Se esperaba '{message}' pero se encontró '{toast_text}'")


@then('aparecen mensajes de error en los campos obligatorios')
def step_verify_error_messages(context):
    errors = []
    if hasattr(context, "pim_page"):
        errors = context.pim_page.get_error_messages()
    elif hasattr(context, "admin_page"):
        errors = context.admin_page.get_error_messages()
    elif hasattr(context, "my_info_page"):
        errors = context.my_info_page.get_error_messages()

    assert_true(len(errors) > 0, "No aparecieron mensajes de error en campos obligatorios")


@when('guarda los cambios')
def step_save_changes(context):
    if hasattr(context, "admin_page"):
        context.admin_page.click_save()
    elif hasattr(context, "my_info_page"):
        context.my_info_page.click_save()
    else:
        raise RuntimeError("No hay página activa para guardar cambios")
