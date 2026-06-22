# feature/

Contiene los escenarios de prueba escritos en **Gherkin** (`.feature`).

## Convenciones

- Un archivo `.feature` por módulo de la aplicación (ej. `login.feature`, `recruitment.feature`).
- Usar `Feature:` para describir la funcionalidad y `Scenario:` para cada caso.
- Agrupar con etiquetas (`@smoke`, `@regression`, etc.) para ejecución selectiva.

## Ejemplo

```gherkin
@smoke
Feature: Login

  Scenario: Login exitoso con credenciales válidas
    Given el usuario está en la página de login
    When ingresa "admin" y "admin123"
    Then es redirigido al dashboard
```

## Reglas

- NO incluir lógica de programación, solo pasos declarativos.
- Los steps se implementan en `steps/`.
- Cada `Scenario` debe ser independiente y atómico.
- Escenarios con limitaciones conocidas del sistema pueden etiquetarse con `@known_issue`.
