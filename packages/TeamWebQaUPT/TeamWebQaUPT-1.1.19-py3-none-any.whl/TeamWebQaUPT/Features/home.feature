Feature: Pruebas de redirección y funcionamiento en la página principal de Juegos Florales 2024

  @chrome
  Scenario: El usuario puede redirigirse a la página de Eventos en Chrome
    Given I am on the "Home" page
    When I click on the "Entérate de los Eventos" button
    Then I should be redirected to "http://161.132.50.153/eventos"

  @firefox
  Scenario: El usuario puede redirigirse a la página de Eventos en Firefox
    Given I am on the "Home" page
    When I click on the "Entérate de los Eventos" button
    Then I should be redirected to "http://161.132.50.153/eventos"

  @edge
  Scenario: El usuario puede redirigirse a la página de Eventos en Edge
    Given I am on the "Home" page
    When I click on the "Entérate de los Eventos" button
    Then I should be redirected to "http://161.132.50.153/eventos"

  @chrome
  Scenario: El usuario puede redirigirse a la página de Ubicaciones en Chrome
    Given I am on the "Home" page
    When I click on the "Conoce las Ubicaciones" button
    Then I should be redirected to "http://161.132.50.153/lugares"

  @firefox
  Scenario: El usuario puede redirigirse a la página de Ubicaciones en Firefox
    Given I am on the "Home" page
    When I click on the "Conoce las Ubicaciones" button
    Then I should be redirected to "http://161.132.50.153/lugares"

  @edge
  Scenario: El usuario puede redirigirse a la página de Ubicaciones en Edge
    Given I am on the "Home" page
    When I click on the "Conoce las Ubicaciones" button
    Then I should be redirected to "http://161.132.50.153/lugares"

  @chrome
  Scenario: El usuario puede redirigirse a la página de Facebook en Chrome
    Given I am on the "Home" page
    When I click on the "Bienestar Universitario UPT" link
    Then I should be redirected to "https://www.facebook.com/ObunUPT/"

  @firefox
  Scenario: El usuario puede redirigirse a la página de Facebook en Firefox
    Given I am on the "Home" page
    When I click on the "Bienestar Universitario UPT" link
    Then I should be redirected to "https://www.facebook.com/ObunUPT/"

  @edge
  Scenario: El usuario puede redirigirse a la página de Facebook en Edge
    Given I am on the "Home" page
    When I click on the "Bienestar Universitario UPT" link
    Then I should be redirected to "https://www.facebook.com/ObunUPT/"

  @chrome
  Scenario Outline: El usuario puede navegar a diferentes secciones desde el menú superior en Chrome
    Given I am on the "Home" page
    When I click on the "<menu>" button
    Then I should be redirected to the "<url>"

    Examples:
      | menu      | url                              |
      | Acerca de | http://161.132.50.153/about       |
      | Eventos   | http://161.132.50.153/eventos     |
      | Equipos   | http://161.132.50.153/equipos     |
      | Lugares   | http://161.132.50.153/lugares     |

  @firefox
  Scenario Outline: El usuario puede navegar a diferentes secciones desde el menú superior en Firefox
    Given I am on the "Home" page
    When I click on the "<menu>" button
    Then I should be redirected to the "<url>"

    Examples:
      | menu      | url                              |
      | Acerca de | http://161.132.50.153/about       |
      | Eventos   | http://161.132.50.153/eventos     |
      | Equipos   | http://161.132.50.153/equipos     |
      | Lugares   | http://161.132.50.153/lugares     |

  @edge
  Scenario Outline: El usuario puede navegar a diferentes secciones desde el menú superior en Edge
    Given I am on the "Home" page
    When I click on the "<menu>" button
    Then I should be redirected to the "<url>"

    Examples:
      | menu      | url                              |
      | Acerca de | http://161.132.50.153/about       |
      | Eventos   | http://161.132.50.153/eventos     |
      | Equipos   | http://161.132.50.153/equipos     |
      | Lugares   | http://161.132.50.153/lugares     |
