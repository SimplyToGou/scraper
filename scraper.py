from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from os import environ
import os
from dotenv import load_dotenv
import argparse
import platform
import time

from browsermobproxy import Server

# bserver = Server("browsermob-proxy/bin/browsermob-proxy")
# bserver.start()
# proxy = bserver.create_proxy()
parser = argparse.ArgumentParser(description="SimplyToGou (TM) proprietary (C) Scraper (TM)")


if ".env" not in os.listdir(os.getcwd()):
    raise Exception(
        "No hay un archivo .env\nPor favor crea uno, fila sigue el formato de example.env"
    )

load_dotenv()

OS = platform.system()
if OS == "Darwin":
    key_command = Keys.COMMAND
else:
    key_command = Keys.CONTROL

url_sernac = environ.get("URL")

chrome_options = Options()
chrome_options.add_argument("log-level=3")
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))

# Mac
driver_location = os.path.join(os.getcwd(), 'chromedriver')
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get(url_sernac)

    selector_regiones = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/div[2]/div[1]'))
    )

    selector_regiones.click()
    time.sleep(1)
    div_opciones = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//body/div[4]")))
    input_region = WebDriverWait(selector_regiones, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input'))
    )
    lista_regiones = div_opciones.text.split("\n")

    diccionario_regiones = {}

    for region in lista_regiones:
        input_region.click()
        input_region.send_keys(region)
        input_region.send_keys(Keys.DOWN)
        input_region.send_keys(Keys.ENTER)
        time.sleep(0.75)

        selector_comunas = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/div[2]/div[2]'))
        )

        input_comunas = WebDriverWait(selector_comunas, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="root"]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/input'))
        )
        input_comunas.click()
        time.sleep(0.75)
        div_opciones = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//body/div[4]")))
        lista_comunas = div_opciones.text.split("\n")
        diccionario_regiones[region] = {}
        for comuna in lista_comunas:

            diccionario_regiones[region][comuna] = 0

        input_region.send_keys(key_command, "a")
        input_region.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
    print(diccionario_regiones)

except Exception as e:
    print(e)

finally:
    driver.close()
