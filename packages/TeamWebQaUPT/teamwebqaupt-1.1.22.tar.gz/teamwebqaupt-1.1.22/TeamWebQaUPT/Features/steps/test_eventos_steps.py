import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep

FACULTADES_VALIDAS = ["FAING", "FAU", "FAEDCOH", "FADE", "FACEM", "FACSA"]

@allure.feature('Filtrado de Eventos por Facultad')
@allure.story('Filtrar Eventos con Dropdown y Checkbox')
@allure.title('Filtrar Eventos y Marcar Checkboxes')
@pytest.mark.chrome
@pytest.mark.firefox
@pytest.mark.edge
def test_filtrar_eventos_y_checkbox(driver):
    with allure.step("Abrir la página de eventos"):
        driver.get("http://161.132.50.153/eventos")
        sleep(3)  

    facultades = [
        "Facultad de Ingeniería",
        "Facultad de Educación, Ciencias de la Comunicación y Humanidades",
        "Facultad de Derecho y Ciencias Políticas",
        "Facultad de Ciencias de la Salud",
        "Facultad de Ciencias Empresariales",
        "Facultad de Arquitectura y Urbanismo",
        "Todas"
    ]

    for facultad_text in facultades:
        for vigentes in [False, True]:
            with allure.step(f"Seleccionar la facultad: {facultad_text} con checkbox {'marcado' if vigentes else 'no marcado'}"):
                try:
                    dropdown = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "facultad"))
                    )
                    dropdown.click()
                    sleep(2)  

                
                    try:
                        option = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, f"//option[text()='{facultad_text}']"))
                        )
                        option.click()
                    except TimeoutException:
                        driver.execute_script(f"document.getElementById('facultad').value = '{facultad_text}'")
                        sleep(2)  
                        allure.attach(f"Forzado: Selección de facultad {facultad_text} con JavaScript", name="Forzado de Selección", attachment_type=allure.attachment_type.TEXT)

                    sleep(2)  

                    if vigentes:
                        try:
                            checkbox = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']"))
                            )
                            checkbox.click()
                            sleep(2)  
                        except NoSuchElementException:
                            allure.attach(f"Advertencia: Checkbox no encontrado para {facultad_text}", name="Error de Checkbox", attachment_type=allure.attachment_type.TEXT)

                    
                    try:
                        eventos_filtrados = WebDriverWait(driver, 5).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.bg-white.p-8.rounded-lg.shadow-lg"))
                        )
                        if facultad_text == "Todas":
                            assert len(eventos_filtrados) > 0, "No se encontraron eventos."
                        else:
                            if len(eventos_filtrados) == 0:
                                no_events_message = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'No hay eventos disponibles en este momento.')]"))
                                )
                                assert no_events_message is not None, "No se encontró mensaje de eventos no disponibles."
                            else:
                                for evento in eventos_filtrados:
                                    try:
                                        facultad_element = evento.find_element(By.XPATH, ".//p[contains(text(), 'Facultad')]")
                                        facultad = facultad_element.text.split(":")[1].strip()
                                        assert facultad == facultad_text, f"Evento con facultad incorrecta: {facultad}"
                                    except NoSuchElementException:
                                        allure.attach("Advertencia: Facultad no encontrada en este evento", name="Advertencia Facultad", attachment_type=allure.attachment_type.TEXT)

                    except TimeoutException:
                        allure.attach(f"Advertencia: No se encontraron eventos para {facultad_text}", name="Error de Eventos", attachment_type=allure.attachment_type.TEXT)

                except NoSuchElementException:
                    allure.attach(f"Advertencia: Opción no encontrada para {facultad_text}", name="Error de Selección", attachment_type=allure.attachment_type.TEXT)
                except TimeoutException:
                    allure.attach(f"Timeout: No se pudo encontrar o seleccionar la opción para {facultad_text}", name="Timeout Error", attachment_type=allure.attachment_type.TEXT)

            sleep(2)  # Esperar antes de seleccionar la siguiente opción

@allure.feature('Navegación en la barra superior')
@allure.story('Navegación del menú superior en la página de eventos')
@pytest.mark.chrome
@pytest.mark.firefox
@pytest.mark.edge
def test_navegacion_menu_superior(driver):
    menus = {
        "Inicio": "http://161.132.50.153/",
        "Acerca de": "http://161.132.50.153/about",
        "Equipos": "http://161.132.50.153/equipos",
        "Participantes": "http://161.132.50.153/participantes",
        "Lugares": "http://161.132.50.153/lugares"
    }

    with allure.step("Abrir la página de eventos"):
        driver.get("http://161.132.50.153/eventos")
        sleep(5)

    for menu, url in menus.items():
        with allure.step(f"Hacer clic en el enlace '{menu}'"):
            try:
                # Volver a la página de eventos para "Acerca de", "Equipos", "Participantes" y "Lugares"
                if menu in ["Acerca de", "Equipos", "Participantes", "Lugares"]:
                    with allure.step(f"Volver a la página de eventos antes de hacer clic en '{menu}'"):
                        driver.get("http://161.132.50.153/eventos")
                        sleep(2)

                # Usar LINK_TEXT para encontrar el enlace y hacer clic
                menu_link = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, menu))
                )
                menu_link.click()
                sleep(1)
                assert driver.current_url == url, f"No se redirigió correctamente al enlace {menu}"

                # Volver a la página de eventos después de cada clic
                driver.get("http://161.132.50.153/eventos")
                sleep(2)

            except (NoSuchElementException, TimeoutException) as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error de Navegación", attachment_type=allure.attachment_type.PNG)
                allure.attach(f"Enlace no encontrado: {menu}", name="Error de Navegación", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"No se pudo hacer clic en el enlace: {menu}")

            sleep(1)

