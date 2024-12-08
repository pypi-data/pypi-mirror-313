import pytest
import subprocess

def test_runner_main_execution():
    """
    Prueba que la función `main` de `runner.py` se ejecute sin errores.
    """
    try:
        result = subprocess.run(
            ["ejecutar_pruebas"],  
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        assert result.returncode == 0, f"El comando fallo con error: {result.stderr}"
    except FileNotFoundError:
        pytest.fail("El comando `ejecutar_pruebas` no fue encontrado. Verifica que está correctamente registrado en `setup.py`.")
    except Exception as e:
        pytest.fail(f"Error inesperado al ejecutar `ejecutar_pruebas`: {e}")

def test_runner_pytest_execution():
    """
    Prueba que pytest pueda ejecutarse directamente usando el archivo runner.py.
    """
    try:
        result = subprocess.run(
            ["pytest", "-n", "3", "--alluredir=allure-results"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        assert result.returncode == 0, f"Pytest fallo con error: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Error inesperado al ejecutar pytest desde runner.py: {e}")
