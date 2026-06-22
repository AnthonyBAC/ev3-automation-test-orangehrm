from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

options = Options()
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

driver.get("https://www.google.com")

print("Título de la página:", driver.title)

sleep(3)

driver.quit()