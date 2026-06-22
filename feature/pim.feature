Feature: Gestión de empleados en PIM

  @smoke
  Scenario: TC-003 Crear empleado con datos válidos
    Given el usuario "Admin" ha iniciado sesión
    When navega al módulo "PIM"
    And hace click en "Add"
    And completa los campos obligatorios
      | firstName | middleName | lastName |
      | John      | Jonas      | Doe      |
    And guarda el registro
    Then aparece el mensaje "Successfully Saved"
    And es redirigido al perfil del empleado creado

  @regression
  Scenario: TC-004 Crear empleado con campos obligatorios vacíos
    Given el usuario "Admin" ha iniciado sesión
    When navega al módulo "PIM"
    And hace click en "Add"
    And deja los campos obligatorios vacíos
    And guarda el registro
    Then permanece en el formulario
    And aparecen mensajes de error en los campos obligatorios
