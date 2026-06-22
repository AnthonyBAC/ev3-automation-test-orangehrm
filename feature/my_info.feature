Feature: Mi información personal

  @smoke
  Scenario: TC-007 Actualizar información personal con datos válidos
    Given el usuario "Admin" ha iniciado sesión
    When navega al módulo "My Info"
    And modifica datos personales válidos
      | middleName |
      | Test       |
    And guarda los cambios
    Then aparece el mensaje "Successfully Updated"
    And permanece en la pantalla "My Info"

  @regression
  Scenario: TC-008 Actualizar información personal con campos vacíos
    Given el usuario "Admin" ha iniciado sesión
    When navega al módulo "My Info"
    And guarda el nombre original
    And deja campos obligatorios vacíos
    And guarda los cambios
    Then aparecen mensajes de error en los campos obligatorios
    And el nombre original permanece sin cambios
