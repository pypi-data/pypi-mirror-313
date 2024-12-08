import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
@allure.feature('Pruebas Participantes')
@allure.story('Verificación de participantes y barra de navegación en la página Participantes')
@pytest.mark.chrome
@pytest.mark.firefox
@pytest.mark.edge
def test_verificar_participantes_y_barra_navegacion(driver):
    with allure.step("Abrir la página de Participantes"):
        driver.get("http://161.132.50.153/participantes")
        sleep(3)

    with allure.step("Verificar la existencia de los participantes"):
        participantes = ["Juan Pérez", "Erick Mamani", "Helbert Condori"]
        for participante in participantes:
            try:
                participante_element = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, f"//h3[contains(text(), '{participante}')]"))
                )
                assert participante_element.is_displayed(), f"{participante} no se muestra correctamente."
            except TimeoutException:
                pytest.fail(f"{participante} no se encontró o no es visible.")
    
    with allure.step("Verificar el funcionamiento de la barra de navegación y volver a Participantes"):
        menus = {
            "Inicio": "http://161.132.50.153/",
            "Acerca de": "http://161.132.50.153/about",
            "Eventos": "http://161.132.50.153/eventos",
            "Equipos": "http://161.132.50.153/equipos",
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
                driver.back()  # Volver a la página "Participantes" para continuar probando la barra
                sleep(1)
