from behave import when, then
from pages.pim_page import PIMPage
from utils.helpers import assert_true


@when('hace click en "Add"')
def step_click_add(context):
    context.pim_page = PIMPage(context.driver)
    context.pim_page.click_add()


@when('completa los campos obligatorios')
def step_fill_employee(context):
    row = context.table[0]
    context.pim_page.fill_employee(
        first_name=row["firstName"],
        middle_name=row["middleName"],
        last_name=row["lastName"],
    )


@when('deja los campos obligatorios vacíos')
def step_clear_employee_fields(context):
    context.pim_page.clear_required_fields()


@when('guarda el registro')
def step_save_employee(context):
    context.pim_page.click_save()


@then('es redirigido al perfil del empleado creado')
def step_verify_profile_redirect(context):
    assert_true(context.pim_page.is_on_profile(), "No se redirigió al perfil del empleado")
    header = context.pim_page.get_profile_header_text()
    assert_true("Personal Details" in header or len(header) > 0, f"Header inesperado: {header}")


@then('permanece en el formulario')
def step_verify_still_on_form(context):
    assert_true(context.pim_page.is_on_profile() is False, "Se redirigió cuando no debería")
