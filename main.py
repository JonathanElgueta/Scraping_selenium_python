from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import datetime
import os
from config import URL_JE, URL_ORDERS_JE, USERNAME_JE, PASSWORD_JE
from functions import SPOC


def main():
    # Crear una instancia de la clase SPOC con la URL proporcionada en la configuración
    spoc = SPOC(URL_JE)

    # Iniciar sesión en el sitio
    driver = spoc.login(USERNAME_JE, PASSWORD_JE)

    if driver is not None:
        try:
            # Extraer los datos
            data_je = spoc.extract_data(driver)

            # Cerrar el programa
            spoc.close_program(driver)
        except Exception as e:
            print(f"Ocurrió una excepción: {e}")
            spoc.close_program(driver)
    else:
        print("Error al iniciar sesión. Saliendo del programa.")


if __name__ == "__main__":
    main()


# Importamos la biblioteca Selenium y las funciones personalizadas SPOC y las constantes URL_JE, USERNAME_JE, PASSWORD_JE, y OUTPUT_DIR_JE desde los archivos functions.py y config.py respectivamente.
# Creamos una instancia de la clase SPOC y la llamamos spoc, utilizando URL_JE como argumento. Esto establece la URL que se utilizará para la automatización y define un objeto SPOC.
# Llamamos a la función login de la clase spoc, pasando USERNAME_JE y PASSWORD_JE como argumentos. Esto inicia sesión en la página de inicio de sesión de SPOC utilizando las credenciales proporcionadas y devuelve un objeto driver que se utilizará para interactuar con la página.
# Llamamos a la función extract_data de la clase spoc, pasando el objeto driver como argumento. Esto extrae los datos de la página de órdenes de SPOC utilizando una serie de comandos Selenium y devuelve un objeto de DataFrame de Pandas que contiene los datos extraídos.
# Llamamos a la función export_to_excel de la clase spoc, pasando el objeto de DataFrame de Pandas df, el directorio de salida OUTPUT_DIR_JE y el nombre de archivo Datos_Spoc.xlsx como argumentos. Esto guarda los datos extraídos en un archivo de Excel en el directorio de salida especificado.
# Llamamos al método quit() del objeto driver para cerrar la sesión de Selenium y el navegador.
