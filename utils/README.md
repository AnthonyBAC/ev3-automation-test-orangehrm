# utils/

Utilidades compartidas para el framework de pruebas.

## Archivos esperados

| Archivo         | Propósito                                      |
| --------------- | ---------------------------------------------- |
| `driver.py`     | Inicialización y configuración del WebDriver    |
| `config.py`     | Carga de variables desde `.env`                 |
| `helpers.py`    | Funciones auxiliares (esperas, capturas, etc.)  |

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
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL  = os.getenv("BASE_URL")
USERNAME  = os.getenv("USERNAME")
PASSWORD  = os.getenv("PASSWORD")
```

## Reglas

- Mantener funciones puras y reutilizables.
- No incluir lógica específica de un caso de prueba.
- Documentar parámetros y retornos.
