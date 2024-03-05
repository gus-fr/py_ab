from sly import Lexer

"""_summary_
Defines the lexer for the experiment language definition
defines common constricts such as operators, identifiers, and common literals (floats, ints)
also defines reserved keywords to be used by the grammar.

uses YACC (via the sly implementation) the heavy FSA lifting
"""


class ExperimentLexer(Lexer):
    """Lexer rules for our language"""

    # define token list to be used by the grammar
    tokens = {
        ID,
        NON_NEG_INTEGER,
        NON_NEG_FLOAT,
        STRING_LITERAL,
        LPAREN,
        RPAREN,
        MINUS,
        COMMA,
        EQ,
        GT,
        LT,
        GE,
        LE,
        NE,
        IN,
        NOT,
        NOT_IN,
        DEF,
        SALT,
        SPLITTERS,
        COLON,
        IF,
        ELIF,
        ELSE,
        WEIGHTED,
        RETURN,
        AND,
        OR,
        LBRACE,
        RBRACE,
    }

    # Special symbols
    LPAREN = r"\("
    RPAREN = r"\)"
    MINUS = r"-"
    COMMA = r","
    COLON = r":"
    LBRACE = r"{"
    RBRACE = r"}"

    # logical operators
    EQ = r"=="
    GT = r">"
    LT = r"<"
    GE = r">="
    LE = r"<="
    NE = r"!="
    IN = r"in"
    NOT_IN = r"not\s+in"
    NOT = r"not"

    # reserved kw
    DEF = r"def"
    SALT = r"salt"
    SPLITTERS = r"splitters"
    IF = r"if"
    ELIF = r"elif"
    ELSE = r"else"
    WEIGHTED = r"weighted"
    RETURN = r"return"
    AND = r"and"
    OR = r"or"

    # identifiers
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # literals
    @_(r"\d+\.\d+")
    def NON_NEG_FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r"\d+")
    def NON_NEG_INTEGER(self, t):
        t.value = int(t.value)
        return t

    @_(r"\".*?\"|\'.*?\'")
    def STRING_LITERAL(self, t):
        t.value = t.value[1:-1]
        return t

    # Comments
    ignore_inline_comment = r"//.*"

    # Ignored pattern
    ignore_newline = r"\n+"
    ignore_ws = r"\s+"
    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
