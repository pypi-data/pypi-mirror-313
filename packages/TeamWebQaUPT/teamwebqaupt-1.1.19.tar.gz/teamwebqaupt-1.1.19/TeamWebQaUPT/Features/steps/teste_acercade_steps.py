import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
@allure.feature('Pruebas Acerca de')
@allure.story('Verificación de contenido y barra de navegación en la página Acerca de')
@pytest.mark.chrome
@pytest.mark.firefox
@pytest.mark.edge
def test_verificar_acerca_de_y_barra_navegacion(driver):
    with allure.step("Abrir la página Acerca de"):
        driver.get("http://161.132.50.153/about")
        sleep(3)

    with allure.step("Verificar la existencia del texto de descripción"):
        try:
            texto_descripcion = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Los VIII Juegos Florales')]"))
            )
            assert texto_descripcion.is_displayed(), "El texto de descripción no se muestra correctamente."
        except TimeoutException:
            pytest.fail("El texto de descripción no se encontró o no es visible.")
    
    with allure.step("Verificar el funcionamiento de la barra de navegación y volver a Acerca de"):
        menus = {
            "Inicio": "http://161.132.50.153/",
            "Eventos": "http://161.132.50.153/eventos",
            "Equipos": "http://161.132.50.153/equipos",
            "Participantes": "http://161.132.50.153/participantes",
            "Lugares": "http://161.132.50.153/lugares"
        }
        
        for menu, url in menus.items():
            with allure.step(f"Hacer clic en el menú '{menu}'"):
                menu_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, menu))
                )
                menu_button.click()
                sleep(1)
                assert driver.current_url == url, f"No se redirigió a la página {url}"
                driver.back()  # Volver a la página "Acerca de" para continuar probando la barra
                sleep(1)
