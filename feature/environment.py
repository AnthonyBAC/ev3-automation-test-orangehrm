import json
import logging
import shutil
from pathlib import Path

from behave.model_core import Status
from utils.driver import get_driver
from utils.logger import setup_logging


def before_all(context):
    for folder in ("reports/screenshots", "reports/fail"):
        path = Path(folder)
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True)

    context.execution_errors = []
    setup_logging()


def before_scenario(context, scenario):
    logging.info(f"Iniciando: {scenario.name}")
    context.driver = get_driver()


def after_step(context, step):
    if step.status not in (Status.failed, Status.error):
        return

    error_message = getattr(step, "error_message", None)
    if not error_message:
        error_message = "No error detail provided by Behave."

    context.execution_errors.append(
        {
            "feature": getattr(getattr(context, "feature", None), "name", ""),
            "scenario": getattr(getattr(context, "scenario", None), "name", ""),
            "step": f"{step.keyword} {step.name}",
            "status": step.status.name,
            "error": error_message,
        }
    )


def after_scenario(context, scenario):
    safe_name = scenario.name.replace(" ", "_").replace("/", "_")
    filename = f"{safe_name}.png"

    screenshot_path = f"reports/screenshots/{filename}"
    context.driver.save_screenshot(screenshot_path)

    is_failed = scenario.status in (Status.failed, Status.error)

    if is_failed:
        fail_path = f"reports/fail/{filename}"
        context.driver.save_screenshot(fail_path)
        logging.error(f"FALLIDO. Captura: {fail_path}")
    else:
        status_name = scenario.status.name
        logging.info(f"{status_name.upper()}: {scenario.name}")

    context.driver.quit()


def after_all(context):
    with open("reports/errors.json", "w", encoding="utf-8") as f:
        json.dump(context.execution_errors, f, ensure_ascii=False, indent=2)
    logging.info("Ejecucion finalizada.")
