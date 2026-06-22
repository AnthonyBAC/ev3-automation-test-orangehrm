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
.venv\Scripts\activate
pip install -r requirements.txt
```

En Linux/macOS puedes usar `source .venv/bin/activate`.

### Preparación rápida en Windows

```bat
scripts\setup_project.bat
```

Ese script:
- crea `.venv` si no existe
- instala dependencias de `requirements.txt`

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
.venv/Scripts/python -m behave                        # todas las features
.venv/Scripts/python -m behave feature/login.feature  # feature especifica
.venv/Scripts/python -m behave --tags=smoke           # solo escenarios smoke
.venv/Scripts/python -m behave --tags=regression      # solo escenarios regression
.venv/Scripts/python run_tests.py                     # behave + reporte HTML
```

### Ejecución rápida en Windows

```bat
scripts\run_tests.bat
```

Ese script:
- ejecuta `run_tests.py`
- corre pruebas
- genera `reports/html/report.html`
- abre reporte HTML al final

## Reportes

Al ejecutar `behave` se generan automaticamente:

```
reports/
├── report.json              # Resultados en formato JSON (sobrescrito)
├── errors.json              # Errores/fallos detallados para reporte HTML
├── test.log                 # Log de ejecucion (sobrescrito)
├── screenshots/             # Capturas de TODOS los escenarios (limpiadas al iniciar)
│   ├── Login_exitoso_con_credenciales_validas.png
│   └── Login_fallido_con_credenciales_invalidas.png
├── fail/                    # Solo escenarios fallidos (limpiadas al iniciar)
│   └── Login_fallido_con_credenciales_invalidas.png
```

| Carpeta / Archivo | Descripcion |
|-------------------|-------------|
| `report.json` | Resultado de todos los escenarios en JSON (pasa/falla, pasos, duracion) |
| `errors.json` | Errores detallados usados por reporte HTML |
| `test.log` | Log con hora de inicio/fin de cada escenario y errores |
| `screenshots/` | Captura de pantalla de **todos** los escenarios (pasen o fallen) |
| `fail/` | Solo los escenarios que **fallaron** (para revision rapida) |
| `html/report.html` | Reporte visual HTML con screenshots embebidas, estados y errores documentados |

La carpeta `reports/` esta en `.gitignore` y no se sube al repositorio.

### Reporte HTML

El reporte HTML **no** se genera al correr `behave` solo. Se genera con `run_tests.py` o `generate_report.py` despues de ejecutar las pruebas:

```bash
# Ejecutar pruebas + generar HTML automaticamente
python run_tests.py

# En Windows, wrapper directo
scripts\run_tests.bat

# O generar el HTML despues de correr behave manualmente
python -m behave
python generate_report.py
```

El reporte incluye:
- Resumen con total/pasaron/fallaron/omitidos y tasa de exito
- Detalle de cada escenario con estado de cada step
- Screenshots embebidas (base64) de cada escenario
- Captura adicional de escenarios fallidos
- Mensajes de error y fallos detectados automaticamente

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
├── run_tests.py            # Ejecuta behave + genera reporte HTML
├── generate_report.py      # Genera reporte HTML desde report.json
├── scripts/
│   ├── setup_project.bat   # Prepara venv + instala requirements
│   └── run_tests.bat       # Corre run_tests.py y abre reporte HTML
├── .gitignore
├── feature/
│   ├── login.feature       # Escenarios Gherkin (@smoke, @regression)
│   ├── pim.feature         # TC-003, TC-004
│   ├── admin.feature       # TC-005, TC-006
│   ├── my_info.feature     # TC-007, TC-008
│   ├── environment.py      # Hooks: abre y cierra el navegador
│   └── steps/
│       ├── login_steps.py  # Step definitions de login
│       ├── common_steps.py # Steps compartidos (login, navegacion, toast, errores)
│       ├── pim_steps.py    # Steps de PIM
│       ├── admin_steps.py  # Steps de Admin
│       └── my_info_steps.py # Steps de My Info
├── pages/
│   ├── login_page.py       # Page Object: pagina de login
│   ├── dashboard_page.py   # Page Object: dashboard
│   ├── menu.py             # Page Object: navegacion de menu lateral
│   ├── pim_page.py         # Page Object: PIM
│   ├── admin_page.py       # Page Object: Admin
│   └── my_info_page.py     # Page Object: My Info
├── utils/
│   ├── config.py           # Credenciales hardcodeadas
│   ├── driver.py           # Inicializacion de Chrome
│   ├── helpers.py          # waits + assertTrue/assertEqual
│   ├── logger.py           # Configuracion de logging
│   └── report_generator.py # Generador de reporte HTML
└── reports/                # Reportes de ejecucion (ignorado por git)
    ├── report.json
    ├── errors.json
    ├── test.log
    ├── screenshots/
    ├── fail/
    └── html/report.html
```
