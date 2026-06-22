#!/usr/bin/env python
"""Ejecuta todas las pruebas behave y genera el reporte HTML.

Uso:
    .venv/Scripts/python run_tests.py
    .venv/Scripts/python run_tests.py --tags=smoke
    .venv/Scripts/python run_tests.py feature/pim.feature
"""
import subprocess
import sys

from utils.report_generator import generate_html_report


def main():
    args = sys.argv[1:]
    cmd = [sys.executable, "-m", "behave"] + args
    print(f"Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    print("\nGenerando reporte HTML...")
    html_path = generate_html_report()
    if html_path:
        print(f"Reporte HTML generado: {html_path}")
    else:
        print("No se pudo generar el reporte HTML")

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
