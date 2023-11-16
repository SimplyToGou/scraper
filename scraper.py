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
import json
from utils import obtener_id, obtener_geografia

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
# chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
chrome_options.set_capability(
                        "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
)

# Mac
driver_location = os.path.join(os.getcwd(), 'chromedriver')
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome(options=chrome_options)

try:
    driver.maximize_window()
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
        time.sleep(0.55)
        div_opciones = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//body/div[4]")))
        lista_comunas = div_opciones.text.split("\n")
        diccionario_regiones[region] = {}
        for comuna in lista_comunas:
            input_comunas.click()
            input_comunas.send_keys(comuna)
            input_comunas.send_keys(Keys.DOWN)
            input_comunas.send_keys(Keys.ENTER)
            time.sleep(0.55)
            obtener_id(driver.get_log("performance"))
            input_comunas.click()
            input_comunas.send_keys(key_command, "a")
            input_comunas.send_keys(Keys.BACKSPACE)
            time.sleep(0.25)

            diccionario_regiones[region][comuna] = 0
        input_region.click()
        input_region.send_keys(key_command, "a")
        input_region.send_keys(Keys.BACKSPACE)
        time.sleep(0.3)
    print(diccionario_regiones)

    # log_entries = driver.get_log("performance")

    """
    for entry in log_entries:
        try:
            obj_serialized: str = entry.get("message")
            obj = json.loads(obj_serialized)
            message = obj.get("message")
            method = message.get("method")
            if method in ['Network.requestWillBeSentExtraInfo' or 'Network.requestWillBeSent']:
                try:
                    for c in message['params']['associatedCookies']:
                        if c['cookie']['name'] == 'authToken':
                            bearer_token = c['cookie']['value']
                except:
                    pass
            print(type(message), method)
            print('--------------------------------------')
            print(message)
        except Exception as e:
            raise e from None
    """

    nfo = obtener_geografia()
    with open("idcomunas.json", 'w+') as yeison:
        json.dump(nfo, yeison, indent=4)



except Exception as e:
    print(e)

finally:
    driver.close()
