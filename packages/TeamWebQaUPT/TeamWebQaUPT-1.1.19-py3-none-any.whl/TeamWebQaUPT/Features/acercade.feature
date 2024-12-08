Feature: Pruebas de redirección y funcionamiento en la página "Acerca de" de Juegos Florales 2024

  @chrome
  Scenario: El usuario puede navegar a las diferentes secciones desde la barra de navegación en la página "Acerca de" en Chrome
    Given I am on the "Acerca de" page at "http://161.132.50.153/about"
    When I click on the "Inicio" button
    Then I should be redirected to "http://161.132.50.153/"
    
    When I click on the "Equipos" button
    Then I should be redirected to "http://161.132.50.153/equipos"
    
    When I click on the "Lugares" button
    Then I should be redirected to "http://161.132.50.153/lugares"
    
    When I click on the "Participantes" button
    Then I should be redirected to "http://161.132.50.153/participantes"

  @firefox
  Scenario: El usuario puede navegar a las diferentes secciones desde la barra de navegación en la página "Acerca de" en Firefox
    Given I am on the "Acerca de" page at "http://161.132.50.153/about"
    When I click on the "Inicio" button
    Then I should be redirected to "http://161.132.50.153/"
    
    When I click on the "Equipos" button
    Then I should be redirected to "http://161.132.50.153/equipos"
    
    When I click on the "Lugares" button
    Then I should be redirected to "http://161.132.50.153/lugares"
    
    When I click on the "Participantes" button
    Then I should be redirected to "http://161.132.50.153/participantes"

  @edge
  Scenario: El usuario puede navegar a las diferentes secciones desde la barra de navegación en la página "Acerca de" en Edge
    Given I am on the "Acerca de" page at "http://161.132.50.153/about"
    When I click on the "Inicio" button
    Then I should be redirected to "http://161.132.50.153/"
    
    When I click on the "Equipos" button
    Then I should be redirected to "http://161.132.50.153/equipos"
    
    When I click on the "Lugares" button
    Then I should be redirected to "http://161.132.50.153/lugares"
    
    When I click on the "Participantes" button
    Then I should be redirected to "http://161.132.50.153/participantes"
