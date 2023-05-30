from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from functions import SPOC
from config import URL_JE, USERNAME_JE, PASSWORD_JE
import pytest


class TestLogin:

    def test_login_success(self):
        spoc_je = SPOC(URL_JE)
        driver_je = spoc_je.login(USERNAME_JE, PASSWORD_JE)
        time.sleep(5)
        assert "Ideal S.A." in driver_je.page_source
        driver_je.quit()


    def test_login_failure(self):
        spoc_je = SPOC(URL_JE)
        driver_je = spoc_je.login("usuario_invalido", "password_invalido")
        time.sleep(5)
        assert "SPOC" in driver_je.title
        driver_je.quit()

        
        

#Ejecutar codigo desde la terminar con comando --> Python -m pytest -v
#El método test_login_success verifica si el inicio de sesión es exitoso al verificar si la cadena "Ideal S.A." está presente en el código fuente de la página. El método usa la clase SPOC y su método login para iniciar sesión con un nombre de usuario y contraseña válidos definidos por las variables USERNAME_JE y PASSWORD_JE. Luego, espera 5 segundos antes de verificar si la cadena "Ideal S.A." está presente en el código fuente de la página. Si la cadena está presente, la prueba pasa, de lo contrario falla
#El método test_login_failure verifica si el inicio de sesión falla al verificar si la cadena "SPOC" está presente en el título de la página después de intentar iniciar sesión con un nombre de usuario y contraseña inválidos. Si la cadena "SPOC" está presente en el título de la página, la prueba pasa, de lo contrario falla.