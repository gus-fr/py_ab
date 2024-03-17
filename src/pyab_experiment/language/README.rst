The full gramar rules as defined in the :py:mod:`pyab_experiment.language` package

.. _grammar:

Language syntax
----------------

.. code-block:: python

    <S> ::= <header>

    <header> ::= <header_id> "{" <opt_header_salt> <opt_splitter> <conditional> "}"

    <empty> ::=

    <header_id> ::= KW_DEF <ID>

    <opt_header_salt> ::= KW_SALT ":" <STRING_LITERAL>
                        | <empty>

    <opt_splitter> ::= KW_SPLITTERS ":" <fields>
                     | <empty>

    <fields> ::= <ID>
               | <ID> "," <fields>

    <conditional> ::= <return_expr>
                    | KW_IF <predicate> "{" <conditional> "}" <subconditional>

    <subconditional> ::=
                   | KW_ELSE "{" <conditional> "}"
                   | KW_ELIF <predicate> "{" <conditional> "}" <subconditional>

    <predicate> ::= KW_NOT <predicate>
                  | <predicate> KW_OR <predicate>
                  | <predicate> KW_AND <predicate>
                  | "(" <predicate> ")"
                  | <term> <logical_op> <term>

    <term> ::= <tuple>
             | <ID>
             | <literal>

    <tuple> ::= "(" <term> <op_term>

    <op_term> ::= ")"
                | "," <term> <op_term>

    <logical_op> ::= KW_NOT_IN
                   | KW_EQ
                   | KW_NE
                   | KW_IN
                   | KW_LE
                   | KW_GE
                   | KW_GT
                   | KW_LT

    <return_expr> ::= KW_RETURN <return_statement>

    <return_statement> ::= <STRING_LITERAL> KW_WEIGHTED <weight> "," <return_statement>
                        | <STRING_LITERAL> KW_WEIGHTED <weight>

    <weight> ::= <NON_NEG_FLOAT>
               | <NON_NEG_INTEGER>

    <literal> ::= <STRING_LITERAL>
                | <NON_NEG_FLOAT>
                | <NON_NEG_INTEGER>
                | "-" <NON_NEG_FLOAT>
                | "-" <NON_NEG_INTEGER>


The following reserved symbols are used in the lexer

.. code-block:: python

    KW_DEF = "def"
    KW_SALT = "salt"
    KW_SPLITTERS = "splitters"
    KW_IF = "if"
    KW_ELSE = "else"
    KW_ELIF = "else if"
    KW_NOT = "not"
    KW_OR = "or"
    KW_AND = "and"
    KW_RETURN = "return"
    KW_WEIGHTED = "weighted"
    KW_NOT_IN = "not in"
    KW_EQ = "=="
    KW_NE = "!="
    KW_IN = "in"
    KW_LE = "<="
    KW_GE = ">="
    KW_GT = ">"
    KW_LT = "<"
