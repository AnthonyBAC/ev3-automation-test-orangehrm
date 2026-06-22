from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils.config import BROWSER, HEADLESS


def create_driver():
    if BROWSER == "chrome":
        options = ChromeOptions()

        if HEADLESS:
            options.add_argument("--headless=new")

        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")

        return webdriver.Chrome(options=options)

    if BROWSER == "firefox":
        options = FirefoxOptions()

        if HEADLESS:
            options.add_argument("--headless")

        return webdriver.Firefox(options=options)

    raise ValueError(f"Navegador no soportado: {BROWSER}")