from behave import when, then
from pages.admin_page import AdminPage
from utils.helpers import assert_true, assert_equal


@when('busca el usuario "{username}"')
def step_search_user(context, username):
    context.admin_page = AdminPage(context.driver)
    context.admin_page.search_user(username)


@when('presiona el icono de editar')
def step_click_edit(context):
    context.admin_page.click_edit_first_result()


@when('cambia el User Role de "{current}" a "{new}"')
def step_change_user_role(context, _current, new):
    context.admin_page.set_user_role(new)


@when('revierte el User Role de "{current}" a "{new}"')
def step_revert_user_role(context, _current, new):
    context.admin_page.edit_and_set_role("Admin", new)


@when('guarda el rol original')
def step_save_original_role(context):
    context.original_role = context.admin_page.get_user_role()


@when('elimina los campos obligatorios')
def step_clear_admin_fields(context):
    context.admin_page.clear_required_fields()


@then('el sistema redirige al módulo Admin')
def step_verify_admin_redirect(context):
    assert_true(context.admin_page.is_on_admin_module(), "No se redirigió al módulo Admin")


@then('el usuario "{username}" tiene el rol "{role}"')
def step_verify_role_in_grid(context, username, role):
    actual_role = context.admin_page.get_role_from_grid(username)
    assert_equal(
        role,
        actual_role,
        f"Se esperaba rol '{role}' pero se encontró '{actual_role or 'vacío'}' para usuario '{username}'",
    )


@then('el rol del usuario permanece igual al original')
def step_verify_original_role(context):
    current_role = context.admin_page.get_user_role()
    assert_equal(context.original_role, current_role, f"El rol cambió de '{context.original_role}' a '{current_role}'")
