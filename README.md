# OrangeHRM - Test Automation

Automatización de pruebas end-to-end para OrangeHRM usando **behave** (BDD) + **Selenium** + **Page Object Model**.

## Stack

| Herramienta       | Uso                        |
| ----------------- | -------------------------- |
| `behave`          | Framework BDD (Gherkin)    |
| `selenium`        | Automatización de navegador |
| `python-dotenv`   | Variables de entorno        |

## Requisitos

- Python 3.10+
- Navegador Chrome/Firefox

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
behave                          # todas las features
behave feature/login.feature     # feature específica
behave -k --tags=smoke           # por tag
```

## Estructura

```
.
├── feature/       # Escenarios BDD en Gherkin
├── pages/         # Page Object Model (localizadores y acciones)
├── utils/         # Configuración, driver y helpers
├── reports/       # Reportes de ejecución
├── .env           # Credenciales y URLs (no versionado)
├── behave.ini     # Configuración de behave
└── requirements.txt
```
