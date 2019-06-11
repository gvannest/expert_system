TRUE = 1
FALSE = 0
UNDETERMINED = 2

IMPLIES = 1
IIF = 2


dic_precedences = {
    ">" : 1,
    '|' : 5,
    '^' : 6,
    '+' : 7,
    '!' : 14,
    '(' : 17,
    ')' : 17,
}