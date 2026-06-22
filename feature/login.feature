Feature: Login de OrangeHRM

  @smoke
  Scenario: Login exitoso con credenciales validas
    Given el usuario esta en la pagina de login
    When ingresa sus credenciales validas
    Then es redirigido al dashboard y ve el texto "Dashboard"

  @regression
  Scenario: Login fallido con credenciales invalidas
    Given el usuario esta en la pagina de login
    When ingresa credenciales invalidas
    Then ve un mensaje de error con el texto "Invalid credentials"
