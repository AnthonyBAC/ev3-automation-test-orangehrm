from behave import given, when, then
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.config import BASE_URL, USERNAME, PASSWORD


@given("el usuario esta en la pagina de login")
def step_open_login(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.open(BASE_URL)


@when("ingresa sus credenciales validas")
def step_valid_credentials(context):
    context.login_page.login(USERNAME, PASSWORD)


@when("ingresa credenciales invalidas")
def step_invalid_credentials(context):
    context.login_page.login("usuario_falso", "clave_falsa")


@then('es redirigido al dashboard y ve el texto "{text}"')
def step_dashboard_visible(context, text):
    dashboard = DashboardPage(context.driver)
    assert dashboard.is_displayed(), "El dashboard no se mostro"
    assert text in dashboard.get_header_text(), (
        f"Se esperaba '{text}' pero se encontro '{dashboard.get_header_text()}'"
    )


@then('ve un mensaje de error con el texto "{text}"')
def step_error_message(context, text):
    error = context.login_page.get_error_message()
    assert text in error, (
        f"Se esperaba mensaje '{text}' pero se encontro '{error}'"
    )
