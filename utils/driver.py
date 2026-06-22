from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


def get_driver():
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)
