# reports/

Reportes generados tras la ejecución de pruebas.

## Contenido

- Archivos de salida del formatter configurado en `behave.ini` (JSON, HTML, Allure, etc.).
- Capturas de pantalla de fallos (si se configuran en hooks).

## Reglas

- No versionar los reportes generados (agregar a `.gitignore`).
- Sobrescribir o limpiar después de cada ejecución.
- Nombrar con timestamp si se conservan (ej. `report_2026-06-21.json`).
