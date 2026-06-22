Feature: Administración de usuarios

  @smoke
  Scenario: TC-005 Editar usuario Admin con datos válidos
    Given el usuario "Admin" ha iniciado sesión
    When navega al módulo "Admin"
    And busca el usuario "Admin"
    And presiona el icono de editar
    And cambia el User Role de "Admin" a "ESS"
    And guarda los cambios
    Then aparece el mensaje "Successfully Updated"
    And el sistema redirige al módulo Admin
    And el usuario "Admin" tiene el rol "ESS"
    When revierte el User Role de "ESS" a "Admin"
    Then aparece el mensaje "Successfully Updated"
    And el usuario "Admin" tiene el rol "Admin"

  @regression
  Scenario: TC-006 Editar usuario Admin con datos inválidos
    Given el usuario "Admin" ha iniciado sesión
    When navega al módulo "Admin"
    And busca el usuario "Admin"
    And presiona el icono de editar
    And guarda el rol original
    And elimina los campos obligatorios
    And guarda los cambios
    Then aparecen mensajes de error en los campos obligatorios
    And el rol del usuario permanece igual al original
