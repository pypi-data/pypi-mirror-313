from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def get_driver(browser_name):
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.set_capability('se:name', 'chrome')
        options.set_capability('se:recordVideo', True)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument('--headless')
        options.set_capability('se:name', 'firefox')
        options.set_capability('se:recordVideo', True)
    elif browser_name == "edge":
        options = EdgeOptions()
        options.add_argument('--headless')
        options.set_capability('se:name', 'edge')
        options.set_capability('se:recordVideo', True)

    return webdriver.Remote(
        command_executor='http://localhost:4444',
        options=options
    )
