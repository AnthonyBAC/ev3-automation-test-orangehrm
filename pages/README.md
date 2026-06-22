# pages/

Implementación del patrón **Page Object Model (POM)**.

## Contenido

- Un archivo `.py` por cada página/vista de OrangeHRM.
- Ejemplos: `login_page.py`, `dashboard_page.py`, `pim_page.py`.

## Estructura de cada Page Object

```python
class LoginPage:
    # Localizadores
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON   = (By.CSS_SELECTOR, "button[type='submit']")

    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
```

## Reglas

- Localizadores como constantes de clase (tuplas `(By.*, "selector")`).
- Métodos representan acciones del usuario (verbos: `login`, `search`, `click_save`).
- Nunca usar `time.sleep()`; usar esperas explícitas (`WebDriverWait`).
- Un Page Object NO debe contener aserciones (eso va en los steps).
