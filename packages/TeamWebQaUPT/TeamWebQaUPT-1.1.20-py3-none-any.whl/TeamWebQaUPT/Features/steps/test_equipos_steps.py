import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep

@allure.feature('Pruebas Equipos')
@allure.story('Verificación de equipos y barra de navegación en la página Equipos')
@pytest.mark.chrome
@pytest.mark.firefox
@pytest.mark.edge
def test_verificar_equipos_y_barra_navegacion(driver):
    with allure.step("Abrir la página de Equipos"):
        driver.get("http://161.132.50.153/equipos")
        sleep(3)

    with allure.step("Verificar la existencia de los equipos"):
        equipos = ["Equipo A", "Equipo B", "Team Prueba"]
        for equipo in equipos:
            try:
                equipo_element = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, f"//h3[contains(text(), '{equipo}')]"))
                )
                assert equipo_element.is_displayed(), f"{equipo} no se muestra correctamente."
            except TimeoutException:
                pytest.fail(f"{equipo} no se encontró o no es visible.")
    
    with allure.step("Verificar el funcionamiento de la barra de navegación y volver a Equipos"):
        menus = {
            "Inicio": "http://161.132.50.153/",
            "Acerca de": "http://161.132.50.153/about",
            "Eventos": "http://161.132.50.153/eventos",
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

                # Volver a la página de Equipos para continuar con las pruebas
                with allure.step("Volver a la página de Equipos"):
                    driver.get("http://161.132.50.153/equipos")
                    sleep(1)
