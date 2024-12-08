import pytest

def main():
    """
    Ejecuta todas las pruebas en paralelo con múltiples navegadores.
    """
    exit_code = pytest.main([
        "-n", "3",                         
        "--alluredir=./allure-results",    
        "--dist=loadscope"                 
    ])
    exit(exit_code)
