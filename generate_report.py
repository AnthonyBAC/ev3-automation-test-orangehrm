#!/usr/bin/env python
"""Genera el reporte HTML a partir de reports/report.json.

Uso:
    .venv/Scripts/python generate_report.py
    # o
    .venv/Scripts/python -m behave && .venv/Scripts/python generate_report.py
"""
from utils.report_generator import generate_html_report


if __name__ == "__main__":
    path = generate_html_report()
    if path:
        print(f"Reporte HTML generado: {path}")
    else:
        print("No se pudo generar el reporte HTML")
