# OrangeHRM - Test Automation

Automatizacion de pruebas end-to-end para OrangeHRM usando **behave** (BDD) + **Selenium** + **Page Object Model**.

## Stack

| Herramienta | Uso |
|------------|-----|
| `behave`   | Framework BDD (Gherkin) |
| `selenium` | Automatizacion de navegador |

## Requisitos

- Python 3.10+
- **Google Chrome** instalado (el driver usa Chrome por defecto)

## Instalacion

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Verificar que el navegador funciona

Ejecuta el script de prueba para validar que Chrome, el driver y las credenciales funcionan:

```bash
python test_chrome.py
```

Si todo esta bien veras en consola:

```
1. Abriendo login...
2. Iniciando sesion...
3. Verificando dashboard...
   Header: Dashboard
4. Prueba pasada.
```

## Ejecutar pruebas

```bash
behave                           # todas las features
behave feature/login.feature     # feature especifica
behave -k --tags=smoke           # solo login exitoso
behave -k --tags=regression      # solo login fallido
```

## Credenciales

Estan hardcodeadas en `utils/config.py` para que cualquier modulo las importe:

```python
from utils.config import BASE_URL, USERNAME, PASSWORD
```

| Variable   | Valor |
|------------|-------|
| `BASE_URL` | `https://opensource-demo.orangehrmlive.com` |
| `USERNAME` | `Admin` |
| `PASSWORD` | `admin123` |

## Estructura

```
.
├── behave.ini              # Configuracion de behave
├── requirements.txt        # behave + selenium
├── test_chrome.py          # Script rapido para probar el setup
├── .gitignore
├── feature/
│   ├── login.feature       # Escenarios Gherkin (@smoke, @regression)
│   ├── environment.py      # Hooks: abre y cierra el navegador
│   └── steps/
│       └── login_steps.py  # Step definitions
├── pages/
│   ├── login_page.py       # Page Object: pagina de login
│   └── dashboard_page.py   # Page Object: dashboard
├── utils/
│   ├── config.py           # Credenciales hardcodeadas
│   ├── driver.py           # Inicializacion de Chrome
│   └── helpers.py          # wait_for_element, wait_for_clickable
└── reports/                # Reportes de ejecucion (ignorado por git)
```
