from pathlib import Path

from utils.driver_factory import create_driver


def before_scenario(context, scenario):
    context.driver = create_driver()


def after_scenario(context, scenario):
    if scenario.status == "failed":
        screenshots_dir = Path("reports/screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        safe_name = scenario.name.replace(" ", "_").replace("/", "_")
        screenshot_path = screenshots_dir / f"{safe_name}.png"

        context.driver.save_screenshot(str(screenshot_path))

    context.driver.quit()