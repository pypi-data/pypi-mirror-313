import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from typing import List, Dict

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def select_dropdown_option(driver, dropdown_selector: str, option_text: str) -> None:
    """
    Selecciona una opción en dropdowns estándar y personalizados.

    :param driver: Selenium WebDriver.
    :param dropdown_selector: Selector CSS del dropdown.
    :param option_text: Texto visible de la opción a seleccionar.
    """
    try:
        logger.info(f"Intentando seleccionar la opción '{option_text}' del dropdown '{dropdown_selector}'")
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_selector))
        )
        dropdown.click()

        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='{option_text}']"))
        )
        option.click()
        logger.info(f"Opción '{option_text}' seleccionada correctamente.")
    except TimeoutException as e:
        logger.error(f"No se pudo seleccionar la opción '{option_text}' en el dropdown '{dropdown_selector}'.")
        raise AssertionError(f"No se pudo seleccionar la opción '{option_text}' en el dropdown '{dropdown_selector}'.") from e


def validate_elements_in_list(driver, xpath_template: str, items: List[str]) -> None:
    """
    Valida que una lista de elementos esté visible en la página.

    :param driver: Selenium WebDriver.
    :param xpath_template: Plantilla XPath con un placeholder para el texto del elemento.
    :param items: Lista de textos de los elementos a validar.
    """
    for item in items:
        try:
            logger.info(f"Validando visibilidad del elemento '{item}'.")
            element_xpath = xpath_template.format(item)
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, element_xpath))
            )
            assert element.is_displayed(), f"El elemento '{item}' no está visible."
            logger.info(f"Elemento '{item}' está visible.")
        except TimeoutException as e:
            logger.error(f"El elemento '{item}' no fue encontrado en la página.")
            raise AssertionError(f"El elemento '{item}' no fue encontrado en la página.") from e


def navigate_menu(driver, menu_items: Dict[str, str], base_url: str) -> None:
    """
    Navega por un menú y valida las redirecciones de las URLs.

    :param driver: Selenium WebDriver.
    :param menu_items: Diccionario {texto_visible: URL_esperada}.
    :param base_url: URL base a la que regresar después de cada navegación.
    """
    for menu_text, expected_url in menu_items.items():
        try:
            logger.info(f"Navegando al menú '{menu_text}' con URL esperada '{expected_url}'.")
            menu_item = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, menu_text))
            )
            menu_item.click()
            WebDriverWait(driver, 10).until(EC.url_to_be(expected_url))
            logger.info(f"Navegación exitosa a '{expected_url}'.")
        except TimeoutException as e:
            logger.error(f"No se pudo navegar a la URL '{expected_url}' para el menú '{menu_text}'.")
            raise AssertionError(f"No se pudo navegar a la URL '{expected_url}' para el menú '{menu_text}'.") from e
        finally:
            logger.info(f"Regresando a la URL base '{base_url}'.")
            driver.get(base_url)


def navigate_linklabel(driver, link_selector: str, expected_url: str) -> None:
    """
    Redirige usando un LinkLabel y valida la URL resultante.

    :param driver: Selenium WebDriver.
    :param link_selector: Selector CSS del LinkLabel.
    :param expected_url: URL esperada después de hacer clic.
    """
    try:
        logger.info(f"Intentando redirigir usando el LinkLabel '{link_selector}' a '{expected_url}'.")
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, link_selector))
        )
        link.click()
        WebDriverWait(driver, 10).until(EC.url_to_be(expected_url))
        logger.info(f"Redirección exitosa a '{expected_url}'.")
    except TimeoutException as e:
        logger.error(f"No se pudo redirigir al LinkLabel '{link_selector}'.")
        raise AssertionError(f"No se pudo redirigir al LinkLabel '{link_selector}'.") from e


def process_table_data(table_data: List[List[str]]) -> List[Dict[str, str]]:
    """
    Convierte datos de una tabla Gherkin en una lista de diccionarios.

    :param table_data: Tabla Gherkin como lista de listas.
    :return: Lista de diccionarios con los datos de la tabla.
    """
    logger.info("Procesando datos de la tabla.")
    headers = table_data[0]
    return [dict(zip(headers, row)) for row in table_data[1:]]

def search_and_validate_results(
    driver,
    search_input_selector: str,
    search_button_selector: str,
    search_term: str,
    results_selector: str,
    expected_results: List[str]
) -> None:
    """
    Realiza una búsqueda en un campo de entrada y valida los resultados.

    :param driver: Selenium WebDriver.
    :param search_input_selector: Selector CSS del campo de entrada de búsqueda.
    :param search_button_selector: Selector CSS del botón de búsqueda.
    :param search_term: Término a buscar.
    :param results_selector: Selector CSS de los resultados de búsqueda.
    :param expected_results: Lista de textos esperados en los resultados.
    """
    try:
        logger.info(f"Realizando búsqueda con el término: '{search_term}'")
        
        # Introducir el término de búsqueda
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, search_input_selector))
        )
        search_input.clear()
        search_input.send_keys(search_term)

        # Hacer clic en el botón de búsqueda
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, search_button_selector))
        )
        search_button.click()

        # Validar los resultados de búsqueda
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, results_selector))
        )
        result_texts = [result.text for result in results]

        for expected in expected_results:
            assert any(expected in result for result in result_texts), \
                f"El resultado esperado '{expected}' no se encontró en los resultados de búsqueda."
        logger.info(f"Búsqueda y validación completadas con éxito para el término: '{search_term}'")
    except TimeoutException as e:
        logger.error("Hubo un problema al realizar la búsqueda o validar los resultados.")
        raise AssertionError("No se completó la búsqueda o no se encontraron resultados válidos.") from e
