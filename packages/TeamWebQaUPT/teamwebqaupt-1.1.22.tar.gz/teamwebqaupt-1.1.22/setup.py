from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="TeamWebQaUPT",
    version="1.1.22",
    description="Paquete para pruebas automatizadas de interfaces web",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UPT-FAING-EPIS/proyecto-si8811a-2024-ii-u2-qa-pruebas-valverde-cano",
    author="Jean Valverde y Anthony Cano",
    author_email="jeanvalverdezamora@gmail.com",
    packages=find_packages(),
    include_package_data=True,  
    package_data={
        "TeamWebQaUPT": ["pytest.ini", "conftest.py"],
    },
    install_requires=[
        "selenium>=4.8.0",
        "pytest>=7.0.0",
        "pytest-xdist>=3.0.0",
        "allure-pytest>=2.13.0",
    ],
    entry_points={
        "console_scripts": [
            "ejecutar_pruebas=TeamWebQaUPT.runner:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
