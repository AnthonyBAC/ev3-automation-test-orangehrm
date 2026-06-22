import logging
from pathlib import Path


def setup_logging():
    Path("reports").mkdir(exist_ok=True)
    log_file = "reports/test.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="w"),
            logging.StreamHandler(),
        ],
    )
