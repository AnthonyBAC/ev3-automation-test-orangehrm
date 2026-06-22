from utils.driver import get_driver
from utils.config import BASE_URL, USERNAME, PASSWORD
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

driver = get_driver()

try:
    print("1. Abriendo login...")
    login_page = LoginPage(driver)
    login_page.open(BASE_URL)

    print("2. Iniciando sesion...")
    login_page.login(USERNAME, PASSWORD)

    print("3. Verificando dashboard...")
    dashboard = DashboardPage(driver)
    assert dashboard.is_displayed(), "El dashboard no se mostro"
    print(f"   Header: {dashboard.get_header_text()}")

    print("4. Prueba pasada.")
except Exception as e:
    print(f"ERROR: {e}")
    raise
finally:
    driver.quit()
