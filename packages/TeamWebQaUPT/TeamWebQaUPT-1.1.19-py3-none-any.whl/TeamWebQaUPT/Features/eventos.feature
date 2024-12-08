Feature: Pruebas de filtrado y navegación en la página de eventos de Juegos Florales 2024

  @chrome @firefox @edge
  Scenario Outline: El usuario puede redirigirse a las secciones del menú superior
    Given I am on the "Eventos" page
    When I click on the "<menu>" link
    Then I should be redirected to "<url>"

    Examples:
      | menu          | url                                    |
      | Inicio        | http://161.132.50.153                  |
      | Acerca de     | http://161.132.50.153/about            |
      | Equipos       | http://161.132.50.153/equipos          |
      | Participantes | http://161.132.50.153/participantes    |
      | Lugares       | http://161.132.50.153/lugares          |

  @chrome @firefox @edge
  Scenario Outline: El usuario puede filtrar eventos por facultad con y sin checkbox marcado
    Given I am on the "Eventos" page
    When I select "<faculty>" from the faculty filter dropdown
    And I mark the "Mostrar solo eventos vigentes" checkbox
    Then I should see events filtered by "<faculty>" or the message "No hay eventos disponibles en este momento."

    Examples:
      | faculty                                                 | vigentes |
      | Facultad de Ingeniería                                  | False    |
      | Facultad de Ingeniería                                  | True     |
      | Facultad de Educación, Ciencias de la Comunicación       | False    |
      | Facultad de Educación, Ciencias de la Comunicación       | True     |
      | Facultad de Derecho y Ciencias Políticas                | False    |
      | Facultad de Derecho y Ciencias Políticas                | True     |
      | Facultad de Ciencias de la Salud                        | False    |
      | Facultad de Ciencias de la Salud                        | True     |
      | Facultad de Ciencias Empresariales                      | False    |
      | Facultad de Ciencias Empresariales                      | True     |
      | Facultad de Arquitectura y Urbanismo                    | False    |
      | Facultad de Arquitectura y Urbanismo                    | True     |
      | Todas                                                   | False    |
      | Todas                                                   | True     |

