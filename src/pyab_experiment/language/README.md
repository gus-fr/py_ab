# Grammar used for our language

Rule 0     S' -> header
Rule 1     header -> header_id LBRACE opt_header_salt opt_splitter conditional RBRACE
Rule 2     empty -> <empty>
Rule 3     header_id -> DEF ID
Rule 4     opt_header_salt -> SALT COLON STRING_LITERAL
Rule 5     opt_header_salt -> empty
Rule 6     opt_splitter -> SPLITTERS COLON fields
Rule 7     opt_splitter -> empty
Rule 8     fields -> ID
Rule 9     fields -> ID COMMA fields
Rule 10    conditional -> return_expr
Rule 11    conditional -> IF predicate LBRACE conditional RBRACE subconditional
Rule 12    subconditional -> empty
Rule 13    subconditional -> ELSE LBRACE conditional RBRACE
Rule 14    subconditional -> ELIF predicate LBRACE conditional RBRACE subconditional
Rule 15    predicate -> NOT predicate  [precedence=left, level=3]
Rule 16    predicate -> predicate OR predicate  [precedence=left, level=1]
Rule 17    predicate -> predicate AND predicate  [precedence=left, level=2]
Rule 18    predicate -> LPAREN predicate RPAREN
Rule 19    predicate -> term logical_op term
Rule 20    term -> tuple
Rule 21    term -> ID
Rule 22    term -> literal
Rule 23    tuple -> LPAREN term op_term
Rule 24    op_term -> RPAREN
Rule 25    op_term -> COMMA term op_term
Rule 26    logical_op -> NOT_IN
Rule 27    logical_op -> EQ
Rule 28    logical_op -> NE
Rule 29    logical_op -> IN
Rule 30    logical_op -> LE
Rule 31    logical_op -> GE
Rule 32    logical_op -> GT
Rule 33    logical_op -> LT
Rule 34    return_expr -> RETURN return_statement
Rule 35    return_statement -> STRING_LITERAL WEIGHTED weight COMMA return_statement
Rule 36    return_statement -> STRING_LITERAL WEIGHTED weight
Rule 37    weight -> NON_NEG_FLOAT
Rule 38    weight -> NON_NEG_INTEGER
Rule 39    literal -> STRING_LITERAL
Rule 40    literal -> NON_NEG_FLOAT
Rule 41    literal -> NON_NEG_INTEGER
Rule 42    literal -> MINUS NON_NEG_FLOAT
Rule 43    literal -> MINUS NON_NEG_INTEGER

Terminals, with rules where they appear:

AND                  : 17
COLON                : 4 6
COMMA                : 9 25 35
DEF                  : 3
ELIF                 : 14
ELSE                 : 13
EQ                   : 27
GE                   : 31
GT                   : 32
ID                   : 3 8 9 21
IF                   : 11
IN                   : 29
LBRACE               : 1 11 13 14
LE                   : 30
LPAREN               : 18 23
LT                   : 33
MINUS                : 42 43
NE                   : 28
NON_NEG_FLOAT        : 37 40 42
NON_NEG_INTEGER      : 38 41 43
NOT                  : 15
NOT_IN               : 26
OR                   : 16
RBRACE               : 1 11 13 14
RETURN               : 34
RPAREN               : 18 24
SALT                 : 4
SPLITTERS            : 6
STRING_LITERAL       : 4 35 36 39
WEIGHTED             : 35 36
