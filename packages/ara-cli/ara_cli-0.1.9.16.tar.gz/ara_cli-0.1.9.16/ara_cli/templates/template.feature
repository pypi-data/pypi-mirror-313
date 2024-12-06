@sample_tag
Feature: <descriptive title>

  As a <user>
  I want to <do something | need something>
  So that <I can achieve something>

  Contributes to <filename or title of the artefact> <agile requirement artefact category> <(optional in case the contribution is to an artefact that is detailed with rules) using rule <rule as it is formulated>   

  Description: <further optional description to understand
  the rule, no format defined, the example artefact is only a placeholder>

  Scenario: <descriptive scenario title>
    Given <precondition>
    When <action>
    Then <expected result>

  Scenario Outline: <descriptive scenario title>
    Given <precondition>
    When <action>
    Then <expected result>

    Examples:
      | descriptive scenario title | precondition         | action             | expected result    |
      | <example title 1>          | <example precond. 1> | <example action 1> | <example result 1> |
      | <example title 2>          | <example precond. 2> | <example action 2> | <example result 2> |
