---
name: bdd-spec-writer
description: Writes executable BDD scenarios (Given/When/Then) with clear acceptance criteria and edge cases. Use before implementing new features or behavior changes.
---
# Rules
- Language: English (Given/When/Then). Clear, unambiguous, domain-driven terminology.
- Declarative over imperative: focus on user intent and business rules, not UI clicks or low-level implementation details.
- Concrete examples over abstract descriptions: include boundary values, invalid inputs, and error states.
- 1 scenario = 1 specific behavior. Keep scenarios independent and idempotent.

# Structure
```gherkin
Feature: <Feature Name>
  As a <role>
  I want <capability>
  So that <business value>

  Scenario: <Happy path>
    Given <initial context/precondition>
    When <action occurs>
    Then <expected outcome/state change>

  Scenario: <Edge case or error handling>
    Given <context>
    When <invalid action or unexpected condition>
    Then <graceful failure or error response>
```

# Output
Append scenarios to the backlog item or specification markdown file under `## Spec`.

# Additional guidance
- Domain terms from `the glossary`. Gherkin: `# language: pt` (`Funcionalidade/Regra/Cenário/Dado/Quando/Então/Esquema do Cenário/Exemplos`), domain text in Portuguese.
- Ids `R<req>.<n>` become the test-name prefix (`R1_2_<english_description>`).
- Error and permission-denied scenarios are mandatory for every rule that touches data. Test data is never real/personal.
- Test mapping: domain rule/service → xUnit unit test (English name, id in name); route/contract → integration test (`WebApplicationFactory`); persistence/tenant → `[DatabaseFact]` (Testcontainers); UI flow → Flutter widget/integration test.
- Output: a `## Spec` block ready to paste into the backlog item + an `id → test layer` table; gaps become **questions** to the user (max 3). Validate with `openspec-validation`.
