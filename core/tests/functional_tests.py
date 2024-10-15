import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NavbarTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--no-sandbox')  # Para evitar errores en entornos de contenedor
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Especificar la ubicación del controlador de Chrome
        driver_path = os.path.abspath('../../drivers/chromedriver')
        print(driver_path)

        # Inicializar el servicio del controlador
        service = Service(executable_path=driver_path)
        service.start()
        print(service)

        # Inicializar el controlador de Chrome con la ruta del servicio y las opciones
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.implicitly_wait(4)  # Esperar hasta 10 segundos para encontrar elementos

    def test_navbar_links(cls):
        cls.driver.get("http://localhost:8000/")  # Reemplaza "http://url_de_tu_aplicacion" con la URL de tu aplicación
        navbar = WebDriverWait(cls.driver, 10).until(
            EC.presence_of_element_located((By.ID, "offcanvasNavbar2"))
        )
        home_link = navbar.find_element(By.LINK_TEXT, "Portada")
        cls.assertTrue(home_link.is_displayed())

        recetas_link = navbar.find_element(By.LINK_TEXT, "Recetas")
        cls.assertTrue(recetas_link.is_displayed())

        hogar_link = navbar.find_element(By.LINK_TEXT, "Hogar y Cocina")
        cls.assertTrue(hogar_link.is_displayed())

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
