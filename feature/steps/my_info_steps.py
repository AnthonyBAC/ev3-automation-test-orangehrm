from behave import when, then
from pages.my_info_page import MyInfoPage
from utils.helpers import assert_true, assert_equal


@when('modifica datos personales válidos')
def step_update_valid_info(context):
    context.my_info_page = MyInfoPage(context.driver)
    row = context.table[0]
    middle_name = row["middleName"]
    context.my_info_page.update_middle_name(middle_name)


@when('guarda el nombre original')
def step_save_original_name(context):
    context.my_info_page = MyInfoPage(context.driver)
    context.original_first_name = context.my_info_page.get_first_name()


@when('deja campos obligatorios vacíos')
def step_clear_my_info_fields(context):
    context.my_info_page.clear_required_fields()


@then('permanece en la pantalla "My Info"')
def step_verify_my_info_screen(context):
    assert_true(context.my_info_page.is_on_my_info(), "No permaneció en My Info")


@then('el nombre original permanece sin cambios')
def step_verify_original_name(context):
    context.driver.refresh()
    context.my_info_page._wait_for_loader()
    current_name = context.my_info_page.get_first_name()
    assert_equal(context.original_first_name, current_name, f"El nombre cambió de '{context.original_first_name}' a '{current_name}'")
