import pytest
from TeamWebQaUPT.webdriver_config import get_driver

@pytest.fixture(scope="session")
def driver(request):
    browser_name = request.param  # Recibe el parámetro del test
    driver_instance = get_driver(browser_name)
    driver_instance.maximize_window()
    yield driver_instance
    driver_instance.quit()

@pytest.fixture(scope="session", params=["chrome", "firefox", "edge"])
def browser_name(request):
    return request.param
