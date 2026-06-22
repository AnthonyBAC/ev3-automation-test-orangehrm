import logging
import shutil
from pathlib import Path

from utils.driver import get_driver
from utils.logger import setup_logging


def before_all(context):
    for folder in ("reports/screenshots", "reports/fail"):
        path = Path(folder)
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True)

    setup_logging()


def before_scenario(context, scenario):
    logging.info(f"Iniciando: {scenario.name}")
    context.driver = get_driver()


def after_scenario(context, scenario):
    safe_name = scenario.name.replace(" ", "_").replace("/", "_")
    filename = f"{safe_name}.png"

    screenshot_path = f"reports/screenshots/{filename}"
    context.driver.save_screenshot(screenshot_path)

    status_name = str(scenario.status)

    if status_name == "failed":
        fail_path = f"reports/fail/{filename}"
        context.driver.save_screenshot(fail_path)
        logging.error(f"FALLIDO. Captura: {fail_path}")
    else:
        logging.info(f"{status_name.upper()}: {scenario.name}")

    context.driver.quit()


def after_all(context):
    logging.info("Ejecucion finalizada.")
