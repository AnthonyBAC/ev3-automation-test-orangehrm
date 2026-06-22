from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

options = Options()
options.add_argument("--width=1920")
options.add_argument("--height=1080")

driver = webdriver.Firefox(options=options)

driver.get("https://www.google.com")

print("Título de la página:", driver.title)

sleep(3)

driver.quit()