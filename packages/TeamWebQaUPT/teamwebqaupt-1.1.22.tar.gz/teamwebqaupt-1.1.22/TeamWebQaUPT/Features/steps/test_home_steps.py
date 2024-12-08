import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

@allure.feature('Pruebas Home')
@allure.story('Verificación de enlaces en la página principal')
@pytest.mark.chrome
@pytest.mark.firefox
@pytest.mark.edge
def test_redirigir_eventos(driver):
    with allure.step("Abrir la página principal"):
        driver.get("http://161.132.50.153/")
        sleep(10)

    with allure.step("Hacer clic en 'Entérate de los Eventos'"):
        try:
            boton_eventos = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Enterate de los Eventos')]"))
            )
            boton_eventos.click()

            with allure.step("Verificar la redirección a la página de eventos"):
                assert driver.current_url == "http://161.132.50.153/eventos", "No se redirigió a la página de eventos."
        except TimeoutException:
            pytest.fail("El botón 'Entérate de los Eventos' no fue encontrado o no es clickable.")


@allure.feature('Pruebas Home')
@allure.story('Verificación de enlaces en la página principal')
@pytest.mark.chrome
@pytest.mark.firefox
@pytest.mark.edge
def test_redirigir_facebook(driver):
    with allure.step("Abrir la página principal"):
        driver.get("http://161.132.50.153/")
        sleep(3)

    with allure.step("Hacer clic en 'Bienestar Universitario UPT'"):
        try:
            link_facebook = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Bienestar Universitario UPT"))
            )
            link_facebook.click()

            # Guardar el manejador de la pestaña original
            original_window = driver.current_window_handle

            # Esperar que se abra una nueva pestaña
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

            # Cambiar el foco a la nueva pestaña
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break

            with allure.step("Verificar la redirección a la página de Facebook"):
                WebDriverWait(driver, 10).until(EC.url_contains("facebook.com"))
                assert driver.current_url == "https://www.facebook.com/ObunUPT/", "No se redirigió a la página de Facebook."

            # Cerrar la nueva pestaña
            driver.close()

            # Regresar a la pestaña original
            driver.switch_to.window(original_window)

        except TimeoutException:
            pytest.fail("El enlace a 'Bienestar Universitario UPT' no fue encontrado o no es clickable.")


@allure.feature('Pruebas Home')
@allure.story('Verificación de enlaces en la página principal')
@pytest.mark.chrome
@pytest.mark.firefox
@pytest.mark.edge
def test_redirigir_ubicaciones(driver):
    with allure.step("Abrir la página principal"):
        driver.get("http://161.132.50.153/")
        sleep(3)

    with allure.step("Hacer clic en 'Conoce las Ubicaciones'"):
        try:
            boton_ubicaciones = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Conoce las Ubicaciones')]"))
            )
            boton_ubicaciones.click()

            with allure.step("Verificar la redirección a la página de ubicaciones"):
                assert driver.current_url == "http://161.132.50.153/lugares", "No se redirigió a la página de ubicaciones."
        except TimeoutException:
            pytest.fail("El botón 'Conoce las Ubicaciones' no fue encontrado o no es clickable.")


@allure.feature('Pruebas Home')
@allure.story('Verificación de enlaces en el menú superior')
@pytest.mark.chrome
@pytest.mark.firefox
@pytest.mark.edge
def test_redirigir_menu_superior(driver):
    menus = {
        "Acerca de": "http://161.132.50.153/about",
        "Eventos": "http://161.132.50.153/eventos",
        "Equipos": "http://161.132.50.153/equipos",
        "Lugares": "http://161.132.50.153/lugares"
    }

    with allure.step("Abrir la página principal"):
        driver.get("http://161.132.50.153/")
        sleep(3)

    for menu, url in menus.items():
        with allure.step(f"Hacer clic en el menú '{menu}'"):
            menu_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, menu))
            )
            menu_button.click()
            sleep(1)
            assert driver.current_url == url, f"No se redirigió a la página {url}"
            driver.back()  # Volver a la página principal para seguir con el siguiente menú
            sleep(1)
