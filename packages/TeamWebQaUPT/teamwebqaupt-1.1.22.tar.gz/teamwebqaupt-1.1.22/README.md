
# TeamWebQaUPT

**TeamWebQaUPT** es un paquete disenado para realizar pruebas automatizadas de interfaces web utilizando Selenium y pytest.  
Proporciona herramientas reutilizables y faciles de usar para simplificar el proceso de pruebas.

# Novedades en la Versión 1.1.22 de TeamWebQaUPT

**TeamWebQaUPT** ha sido actualizado para incluir mejoras significativas y nuevas funcionalidades que amplían las capacidades del paquete y simplifican las pruebas automatizadas en diversas plataformas.

---

## **Nuevas Funcionalidades**

### **1. Soporte para Pruebas Paralelas en Múltiples Navegadores**
- Las pruebas ahora pueden ejecutarse simultáneamente en **Chrome**, **Firefox** y **Edge**.
- Esto es posible gracias a la parametrización de navegadores en la fixture `driver` del archivo `conftest.py`.

---

### **2. Compatibilidad con Dropdowns y Menús en Frameworks Modernos**
- Las funciones para interactuar con **dropdowns** y **listboxes** ahora son compatibles con aplicaciones hechas en React, HTML estándar y otros frameworks.
- **Uso Ejemplo**:
    ```python
    from TeamWebQaUPT.utils import select_dropdown_option

    select_dropdown_option(driver, "button[role='combobox']", "Option Text")
    ```

---

### **3. Redirección Mediante LinkLabels**
- Nueva función `navigate_linklabel` para manejar redirecciones usando etiquetas de enlace (LinkLabels).
- **Uso Ejemplo**:
    ```python
    from TeamWebQaUPT.utils import navigate_linklabel

    navigate_linklabel(driver, "a[data-testid='link']", "https://example.com/target")
    ```

---

### **4. Navegación Mejorada por Menús**
- La función `navigate_menu` ha sido optimizada para validar automáticamente las redirecciones de URLs en menús dinámicos.
- **Uso Ejemplo**:
    ```python
    from TeamWebQaUPT.utils import navigate_menu

    navigate_menu(
        driver,
        menu_items={"Inicio": "http://161.132.50.153/"},
        base_url="http://161.132.50.153/eventos"
    )
    ```

---

## **Mejoras Técnicas**

### **1. Pruebas Paralelas Mejoradas**
- Ejecución de pruebas en paralelo utilizando `pytest-xdist`.
- Configuración predeterminada: 3 procesos paralelos.

---

### **2. Compatibilidad con Frameworks Modernos**
- Las funciones ahora manejan casos dinámicos y asíncronos típicos de frameworks como **React**, **Angular** y **Vue.js**.

---

### **3. Reportes Detallados con Allure**
- Los resultados de las pruebas se generan en el formato `allure-results`, listos para ser visualizados con Allure.

---

## **Cambios Internos**

### **1. Fixture Parametrizada en `conftest.py`**
- La fixture `driver` ahora soporta múltiples navegadores (Chrome, Firefox y Edge).

### **2. Comando `ejecutar_pruebas` Mejorado**
- Soporte para ejecutar pruebas paralelas en múltiples navegadores.

---

## **Documentación Actualizada**
- El archivo `README.md` incluye ejemplos de las nuevas funciones reutilizables.
- Instrucciones detalladas para configurar Selenium Grid con el archivo `docker-compose.yml`.

---

## **Estructura Sugerida del Proyecto**
```bash
Nombre_De_tu_carpeta
|
|---Carpeta_"tests"
|
|---docker-compose.yml
```


## **Instalacion**

### Requisitos Previos
1. Tener instalado **Python 3.8** o superior.
2. Instalar pip (administrador de paquetes de Python).
3. Tener Selenium Grid configurado y en ejecucion (opcional para pruebas distribuidas).

### Instalacion del Paquete
1. Instala el paquete desde PyPI:
   ```bash
   pip install TeamWebQaUPT
   ```

2. Verifica la instalacion:
   ```bash
   python -c "import TeamWebQaUPT; print('Instalacion exitosa')"
   ```

---

## **Ejecucion de Pruebas**

### Comando para Ejecutar Todas las Pruebas
El paquete incluye un script que ejecuta todas las pruebas automaticamente y genera un reporte Allure:
```bash
ejecutar_pruebas
```

Por defecto, el comando:
- Ejecuta pruebas en paralelo utilizando 3 procesos (`-n 3`).
- Genera resultados en el directorio `allure-results`.

### Ver Resultados con Allure
Para visualizar los resultados en formato Allure:
1. Instala Allure:
   ```bash
   brew install allure  # En macOS
   sudo apt install allure  # En Linux
   ```
   [Instrucciones de instalacion para Windows](https://docs.qameta.io/allure/#_get_started).

2. Visualizar los resultados generados:
   ```bash
   allure serve allure-results
   ```

---

## **Funciones Reutilizables**

El paquete incluye una serie de funciones reutilizables en el modulo `utils.py`. Aqui hay una lista de las mas utiles:

### 1. **Seleccionar Opcion en Dropdown**
```python
from TeamWebQaUPT.utils import select_dropdown_option

select_dropdown_option(driver, dropdown_selector="button[role='combobox']", option_text="Todas")
```

**Descripcion**:
- Selecciona una opcion en un combo box (dropdown) por texto visible.

**Parametros**:
- `driver`: Instancia de Selenium WebDriver.
- `dropdown_selector`: Selector CSS del dropdown.
- `option_text`: Texto visible de la opcion a seleccionar.

---

### 2. **Validar Elementos en una Lista**
```python
from TeamWebQaUPT.utils import validate_elements_in_list

validate_elements_in_list(driver, "//h3[contains(text(), '{}')]", ["Elemento A", "Elemento B"])
```

**Descripcion**:
- Verifica que una lista de elementos este visible en la pagina.

**Parametros**:
- `driver`: Instancia de Selenium WebDriver.
- `xpath_template`: Plantilla de XPath para encontrar los elementos (usa `{}` para insertar el texto del elemento).
- `items`: Lista de textos a validar.

---

### 3. **Navegar por Menus**
```python
from TeamWebQaUPT.utils import navigate_menu

navigate_menu(
    driver,
    menu_items={
        "Inicio": "http://161.132.50.153/",
        "Eventos": "http://161.132.50.153/eventos"
    },
    base_url="http://161.132.50.153/equipos"
)
```

**Descripcion**:
- Navega por un menu y valida la navegacion de URLs.

**Parametros**:
- `driver`: Instancia de Selenium WebDriver.
- `menu_items`: Diccionario con texto del menu como clave y URL esperada como valor.
- `base_url`: URL base para regresar despues de cada navegacion.

---

### 4. **LinkLabels**
```python
from TeamWebQaUPT.utils import navigate_linklabel

navigate_linklabel(driver, "a[data-testid='link-label']", "http://161.132.50.153/nueva-pagina")
```

**Descripcion**:
- Redirige usando un LinkLabel y valida la URL resultante.

**Parametros**:
- `driver`: Instancia de Selenium WebDriver.
- `link_selector`: Selector CSS del LinkLabel.
- `expected_url`: URL esperada despues de hacer clic.

---

### 5. **Procesar Tablas Gherkin**
```python
from TeamWebQaUPT.utils import process_table_data

table_data = [
    ["Columna1", "Columna2"],
    ["Valor1", "Valor2"]
]
processed_data = process_table_data(table_data)
```

**Descripcion**:
- Convierte datos de una tabla en un formato reutilizable.

**Parametros**:
- `table_data`: Lista de listas con los datos de la tabla (primera fila como encabezados).

**Retorno**:
- Una lista de diccionarios con claves basadas en la primera fila.

---

## **Pruebas Paralelas con Docker Compose**

El paquete incluye un archivo `docker-compose.yml` para ejecutar pruebas en paralelo utilizando Selenium Grid.

### **Contenido del `docker-compose.yml` para las pruebas paralelas**
```yaml
version: "3"
services:
  selenium-hub:
    image: selenium/hub:4.25.0-20240922
    container_name: selenium-hub
    ports:
      - "4442:4442"
      - "4443:4443"
      - "4444:4444"
    networks:
      - selenium-grid

  chrome:
    image: selenium/node-chrome:4.25.0-20240922
    container_name: chrome
    shm_size: 2gb
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=3
    networks:
      - selenium-grid

  firefox:
    image: selenium/node-firefox:4.25.0-20240922
    container_name: firefox
    shm_size: 2gb
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=3
    networks:
      - selenium-grid

  edge:
    image: selenium/node-edge:4.25.0-20240922
    container_name: edge
    shm_size: 2gb
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=3
    networks:
      - selenium-grid

  chrome_video:
    image: selenium/video:ffmpeg-7.0.2-20240922
    container_name: chrome_video
    volumes:
      - ./videos:/videos
    depends_on:
      - chrome
    environment:
      - DISPLAY_CONTAINER_NAME=chrome
      - SE_NODE_GRID_URL=http://selenium-hub:4444
      - SE_VIDEO_FILE_NAME=auto
      - FFmpeg_Options=" -framerate 2 -video_size 1920x1080 -probesize 5000000 -analyzeduration 1000000 "
    networks:
      - selenium-grid

  edge_video:
    image: selenium/video:ffmpeg-7.0.2-20240922
    container_name: edge_video
    volumes:
      - ./videos:/videos
    depends_on:
      - edge
    environment:
      - DISPLAY_CONTAINER_NAME=edge
      - SE_NODE_GRID_URL=http://selenium-hub:4444
      - SE_VIDEO_FILE_NAME=auto
      - FFmpeg_Options=" -framerate 2 -video_size 1920x1080 -probesize 5000000 -analyzeduration 1000000 "
    networks:
      - selenium-grid

  firefox_video:
    image: selenium/video:ffmpeg-7.0.2-20240922
    container_name: firefox_video
    volumes:
      - ./videos:/videos
    depends_on:
      - firefox
    environment:
      - DISPLAY_CONTAINER_NAME=firefox
      - SE_NODE_GRID_URL=http://selenium-hub:4444
      - SE_VIDEO_FILE_NAME=auto
      - FFmpeg_Options=" -framerate 2 -video_size 1920x1080 -probesize 5000000 -analyzeduration 1000000 "
    networks:
      - selenium-grid

networks:
  selenium-grid:
    driver: bridge
```

### **Como Usarlo**
1. Levanta el entorno Selenium Grid:
   ```bash
   docker-compose up -d
   ```

2. Ejecuta las pruebas en paralelo:
   ```bash
   pytest -n 3 --alluredir=allure-results
   ```

---

## **Licencia**
Este proyecto esta licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para mas detalles.
