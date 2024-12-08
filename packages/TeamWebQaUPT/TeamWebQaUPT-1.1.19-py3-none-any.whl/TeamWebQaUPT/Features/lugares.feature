Feature: Pruebas de redirección y funcionamiento en la página "Lugares" de Juegos Florales 2024

  @chrome
  Scenario: El usuario puede navegar a las diferentes secciones desde la barra de navegación en la página "Lugares" en Chrome
    Given I am on the "Lugares" page at "http://161.132.50.153/lugares"
    When I click on the "Inicio" button
    Then I should be redirected to "http://161.132.50.153/"
    And I navigate back to the "Lugares" page

    When I click on the "Equipos" button
    Then I should be redirected to "http://161.132.50.153/equipos"
    And I navigate back to the "Lugares" page

    When I click on the "Acerca de" button
    Then I should be redirected to "http://161.132.50.153/about"
    And I navigate back to the "Lugares" page

    When I click on the "Participantes" button
    Then I should be redirected to "http://161.132.50.153/participantes"
    And I navigate back to the "Lugares" page

  @firefox
  Scenario: El usuario puede navegar a las diferentes secciones desde la barra de navegación en la página "Lugares" en Firefox
    Given I am on the "Lugares" page at "http://161.132.50.153/lugares"
    When I click on the "Inicio" button
    Then I should be redirected to "http://161.132.50.153/"
    And I navigate back to the "Lugares" page

    When I click on the "Equipos" button
    Then I should be redirected to "http://161.132.50.153/equipos"
    And I navigate back to the "Lugares" page

    When I click on the "Acerca de" button
    Then I should be redirected to "http://161.132.50.153/about"
    And I navigate back to the "Lugares" page

    When I click on the "Participantes" button
    Then I should be redirected to "http://161.132.50.153/participantes"
    And I navigate back to the "Lugares" page

  @edge
  Scenario: El usuario puede navegar a las diferentes secciones desde la barra de navegación en la página "Lugares" en Edge
    Given I am on the "Lugares" page at "http://161.132.50.153/lugares"
    When I click on the "Inicio" button
    Then I should be redirected to "http://161.132.50.153/"
    And I navigate back to the "Lugares" page

    When I click on the "Equipos" button
    Then I should be redirected to "http://161.132.50.153/equipos"
    And I navigate back to the "Lugares" page

    When I click on the "Acerca de" button
    Then I should be redirected to "http://161.132.50.153/about"
    And I navigate back to the "Lugares" page

    When I click on the "Participantes" button
    Then I should be redirected to "http://161.132.50.153/participantes"
    And I navigate back to the "Lugares" page
