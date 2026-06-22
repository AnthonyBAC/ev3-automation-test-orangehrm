# utils/

Utilidades compartidas para el framework de pruebas.

## Archivos esperados

| Archivo         | Propósito                                      |
| --------------- | ---------------------------------------------- |
| `driver.py`     | Inicialización y configuración del WebDriver    |
| `config.py`     | Configuración base del demo (`BASE_URL`, `USERNAME`, `PASSWORD`) |
| `helpers.py`    | Esperas compartidas + `assertTrue`/`assertEqual` |
| `logger.py`     | Configuración de `reports/test.log`             |
| `report_generator.py` | Generación de `reports/html/report.html` |

## Ejemplo: `driver.py`

```python
from selenium import webdriver

def get_driver(browser="chrome"):
    if browser == "chrome":
        return webdriver.Chrome()
    elif browser == "firefox":
        return webdriver.Firefox()
    raise ValueError(f"Navegador no soportado: {browser}")
```

## Ejemplo: `config.py`

```python
BASE_URL = "https://opensource-demo.orangehrmlive.com"
USERNAME = "Admin"
PASSWORD = "admin123"
```

## Reglas

- Mantener funciones reutilizables.
- No incluir lógica específica de un escenario en helpers compartidos.
- Si una utilidad solo se usa una vez, preferir dejarla cerca de su contexto.
