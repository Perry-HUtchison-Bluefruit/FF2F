Feature: feature 1

Scenario: scenario 1
Given step 1
When step 2
Then step 3

Scenario: scenario 2
Given step 4
When step 5
Then step 6

Scenario: scenario 3
Given step 7
When step 8
Then step 9

Scenario Outline: Correct scenario outline: scenario 4
Given step 10 <column 1>
When step 11
Then step 12
Examples:
| column 1 |
| value 1  |
| value 2  |
| value 3  |

Scenario Outline: Incorret example name: scenario 5
Given step 13
And step 14 <column 2>
When step 15
Then step 16
Examples:
| column 1 |
| value 1  |
| value 2  |

Scenario Outline: Missing examples keyword: scenario 6
Given step 17
And step 18 <column 1>
When step 19
Then step 20
| column 1 |
| value 1  |

Scenario Outline: Missing example table: scenario 7
Given step 17
And step 18 <column 1>
When step 19
Then step 20
Examples:
| column 1 |

Scenario Outline: scenario outline should be scenario: scenario 8
Given step 21
When step 22
Then step 23

Scenario Outline: Valid scenario outline with three example lines: scenario 9
Given step 24 <column 1>
When step 25
Then step 26
Examples:
| column 1 |
| value 1  |
| value 2  |


Scenario Outline: Invalid scenario outline with less than three example lines: scenario 10
Given step 27 <column 1>
When step 28
Then step 29
Examples:
| column 1 |
| value 1  |

Feature: feature 2

Scenario: scenario 9
Given step 24
And step 25
When step 26
Then step 27

Scenario: scenario 10
Given step 28
And step 29
When step 30
Then step 31
And step 32

Developer Task: task 1

Feature: feature 3

Developer Task: task 2

Scenario: scenario 11
Giben step 33
When step 34
Then step 35

1Scenario: scenario 12
    Given step 36
    When step 37
    Then step 38

        Sceanario: scenario 13
        Given step 39
        When step 40
        Then step 41
        And step 42

Scenario: scenario 14
Given step 43
When step 44
Then step 45

Scenario: scenario 15
Given step 46
When step 47
Then step 48

Scenarios: scenario 16
Givn step 49
When step 50
Then step 51

scenario: scenario 17
Givn step 52
When step 53
Then step 54

Scenario: scenario 18
Given step 55
Wen step 56
The step 57
