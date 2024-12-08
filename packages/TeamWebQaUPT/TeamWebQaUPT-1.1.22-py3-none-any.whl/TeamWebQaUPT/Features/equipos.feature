Feature: Pruebas de redirección y funcionamiento en la página de Equipos de Juegos Florales 2024

  @chrome
  Scenario: El usuario puede navegar a las diferentes secciones desde la barra de navegación en Chrome
    Given I am on the "Equipos" page at "http://161.132.50.153/equipos"
    When I click on the "Inicio" button
    Then I should be redirected to "http://161.132.50.153/"
    And I navigate back to the "Equipos" page

    When I click on the "Acerca de" button
    Then I should be redirected to "http://161.132.50.153/about"
    And I navigate back to the "Equipos" page

    When I click on the "Lugares" button
    Then I should be redirected to "http://161.132.50.153/lugares"
    And I navigate back to the "Equipos" page

    When I click on the "Participantes" button
    Then I should be redirected to "http://161.132.50.153/participantes"
    And I navigate back to the "Equipos" page

  @firefox
  Scenario: El usuario puede navegar a las diferentes secciones desde la barra de navegación en Firefox
    Given I am on the "Equipos" page at "http://161.132.50.153/equipos"
    When I click on the "Inicio" button
    Then I should be redirected to "http://161.132.50.153/"
    And I navigate back to the "Equipos" page

    When I click on the "Acerca de" button
    Then I should be redirected to "http://161.132.50.153/about"
    And I navigate back to the "Equipos" page

    When I click on the "Lugares" button
    Then I should be redirected to "http://161.132.50.153/lugares"
    And I navigate back to the "Equipos" page

    When I click on the "Participantes" button
    Then I should be redirected to "http://161.132.50.153/participantes"
    And I navigate back to the "Equipos" page

  @edge
  Scenario: El usuario puede navegar a las diferentes secciones desde la barra de navegación en Edge
    Given I am on the "Equipos" page at "http://161.132.50.153/equipos"
    When I click on the "Inicio" button
    Then I should be redirected to "http://161.132.50.153/"
    And I navigate back to the "Equipos" page

    When I click on the "Acerca de" button
    Then I should be redirected to "http://161.132.50.153/about"
    And I navigate back to the "Equipos" page

    When I click on the "Lugares" button
    Then I should be redirected to "http://161.132.50.153/lugares"
    And I navigate back to the "Equipos" page

    When I click on the "Participantes" button
    Then I should be redirected to "http://161.132.50.153/participantes"
    And I navigate back to the "Equipos" page
