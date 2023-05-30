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
import config


class SPOC:

    def __init__(self, url):
        self.url = url

    def login(self, username, password):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Ejecución en modo headless
            driver = webdriver.Chrome(
                executable_path='/path/to/chromedriver', options=options)
            driver.get(self.url)
            time.sleep(3)
            input_user = driver.find_element(by=By.ID, value="input-12")
            input_user.send_keys(username)
            input_password = driver.find_element(by=By.ID, value="input-16")
            input_password.send_keys(password)
            input_button = driver.find_element(
                by=By.CLASS_NAME, value="button-container")
            input_button.click()
            time.sleep(3)
            return driver
        except Exception as e:
            print(f"An exception occurred: {e}")
            return None

    def extract_data(self, driver):
        driver.get(config.URL_ORDERS_JE)
        time.sleep(20)

        is_next_page = True
        page_count = 1
        output_dir = config.OUTPUT_DIR
        previous_order = None

        while is_next_page:
            data_je = self.get_data_je(driver)

            if previous_order is not None and data_je:
                # Guardar el valor de la Orden de Compra del archivo actual
                current_order = data_je[-1][1]

                if current_order == previous_order:
                    print(
                        "Se encontró coincidencia en la Orden de Compra. Finalizando el programa.")
                    return self.export_data(data_je, page_count)

            if data_je:
                # Guardar el valor de la Orden de Compra del archivo actual
                previous_order = data_je[-1][1]

                # Exportar datos
                self.export_data(data_je, page_count)

            page_count += 1

        return None

    def get_data_je(self, driver):
        data_je = []
        rows_je = len(driver.find_elements(
            By.XPATH, "//*[@id='main-panel']/div/div/div[2]/div[1]/div/div/div[4]/div[2]/div[1]/table/tbody/tr"))
        columns_je = len(driver.find_elements(
            By.XPATH, "//*[@id='main-panel']/div/div/div[2]/div[1]/div/div/div[4]/div[2]/div[1]/table/tbody/tr[1]/td"))

        is_next_page = True  # Inicializar la variable is_next_page

        for i in range(1, rows_je + 1):
            row_data_je = []
            for b in range(1, columns_je + 1):
                try:
                    dato_je = driver.find_element(
                        By.XPATH, "//*[@id='main-panel']/div/div/div[2]/div[1]/div/div/div[4]/div[2]/div[1]/table/tbody/tr[" + str(
                            i) + "]/td[" + str(b) + "]").text
                except NoSuchElementException:
                    is_next_page = False
                    break
                row_data_je.append(dato_je)
            if len(row_data_je) > 0:
                data_je.append(row_data_je)

        if is_next_page:
            try:
                following = driver.find_element(
                    By.CLASS_NAME, "v-data-footer__icons-after")
                following.click()
                time.sleep(5)
            except NoSuchElementException:
                is_next_page = False

        return data_je

    def export_data(self, data_je, page_count):
        name_cols = ['Indice', 'Numero_OC', 'Fecha_Recepcion', 'Fecha_Emision', 'Fecha_Despacho',
                     'Nombre_Cliente', 'Nombre_Sucursal', 'Unidad_Negocio', 'Origen', 'Total', 'Estado']

        # Exportar datos a archivo Excel
        file_name = f'data_selenium_{datetime.datetime.now().strftime("%d-%m-%Y")}_{page_count}.xlsx'
        file_path = os.path.join(config.OUTPUT_DIR, file_name)
        df = pd.DataFrame(data_je, columns=name_cols)
        df = df.rename(columns={'Indice': 'Indice', 'Numero_OC': 'Orden de Compra', 'Fecha_Recepcion': 'Fecha Recepcion',
                                'Fecha_Emision': 'Fecha Emision', 'Fecha_Despacho': 'Fecha Despacho',
                                'Nombre_Cliente': 'Cadena', 'Nombre_Sucursal': 'Nombre Sala',
                                'Unidad_Negocio': 'Centro de ventas', 'Origen': 'Origen', 'Total': 'Total',
                                'Estado': 'Estado'})
        df = df.drop(columns=['Indice'])

        df.to_excel(file_path, index=False)
        print(f"Archivo '{file_name}'exportado correctamente.")

        return df

    def close_program(self, driver):
        print("La extracción de datos se ha ejecutado correctamente")
        driver.quit()


# __init__: Este método se llama cuando se crea una instancia de la clase. Recibe un argumento url que se utiliza para almacenar la URL del sitio web.
# login: Este método se utiliza para iniciar sesión en el sitio web. Recibe dos argumentos: username y password, que se utilizan para ingresar las credenciales de inicio de sesión. El método utiliza Selenium WebDriver para abrir una instancia del navegador Chrome, navegar a la URL del sitio web, ingresar las credenciales de inicio de sesión y hacer clic en el botón de inicio de sesión. Devuelve la instancia del controlador del navegador.
# extract_data: Este método se utiliza para extraer los datos de interés del sitio web después de haber iniciado sesión. Recibe un argumento driver que es la instancia del controlador del navegador devuelto por el método login. El método utiliza Selenium WebDriver para navegar a la página de pedidos del sitio web, extraer los datos de la tabla de pedidos y almacenarlos en un DataFrame de Pandas. Devuelve el DataFrame.
# export_to_excel: Este método se utiliza para exportar los datos extraídos a un archivo de Excel. Recibe tres argumentos: df, que es el DataFrame devuelto por el método extract_data, output_dir, que es la ruta del directorio donde se guardará el archivo de Excel, y output_filename, que es el nombre del archivo de Excel. El método utiliza la función os.path.join para combinar output_dir y output_filename en una sola ruta, luego utiliza el método to_excel de Pandas para exportar el DataFrame a un archivo de Excel en la ruta especificada.
