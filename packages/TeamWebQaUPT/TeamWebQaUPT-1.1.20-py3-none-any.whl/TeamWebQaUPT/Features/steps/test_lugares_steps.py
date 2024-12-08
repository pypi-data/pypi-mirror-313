import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep

@allure.feature('Pruebas Lugares')
@allure.story('Verificación de lugares y barra de navegación en la página Lugares')
@pytest.mark.chrome
@pytest.mark.firefox
@pytest.mark.edge
def test_verificar_lugares_y_barra_navegacion(driver):
    with allure.step("Abrir la página de Lugares"):
        driver.get("http://161.132.50.153/lugares")
        sleep(3)

    with allure.step("Verificar la existencia de los lugares"):
        lugares = [
            "Gimnasio UPT", "Aula Magna", "Cafetería UPT", "Sala de Ensayos", 
            "Auditorio Principal", "Sala de Juegos", "Sala de Música", 
            "Centro de Idiomas", "Auditorio de Deportes", "Plaza UPT", 
            "Estadio Universitario", "Laboratorio de Computación", "Laboratorio de Ciencias",
            "Espacio de Innovación", "Centro de Recursos", "Sala de Conferencias", 
            "Zona Recreativa"
        ]
        for lugar in lugares:
            try:
                lugar_element = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, f"//h3[contains(text(), '{lugar}')]"))
                )
                assert lugar_element.is_displayed(), f"{lugar} no se muestra correctamente."
            except TimeoutException:
                pytest.fail(f"{lugar} no se encontró o no es visible.")

    with allure.step("Verificar el funcionamiento de la barra de navegación y volver a Lugares"):
        menus = {
            "Inicio": "http://161.132.50.153/",
            "Acerca de": "http://161.132.50.153/about",
            "Eventos": "http://161.132.50.153/eventos",
            "Equipos": "http://161.132.50.153/equipos",
            "Participantes": "http://161.132.50.153/participantes"
        }

        for menu, url in menus.items():
            with allure.step(f"Hacer clic en el menú '{menu}'"):
                menu_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, menu))
                )
                menu_button.click()
                sleep(1)
                assert driver.current_url == url, f"No se redirigió a la página {url}"

                # Volver a la página de Lugares para continuar con las pruebas
                with allure.step("Volver a la página de Lugares"):
                    driver.get("http://161.132.50.153/lugares")
                    sleep(1)
