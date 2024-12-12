The full gramar rules as defined in the :py:mod:`pyab_experiment.language` package

.. _grammar:

Language syntax
================

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

    <return_statement> ::= literal KW_WEIGHTED <weight> "," <return_statement>
                        | literal KW_WEIGHTED <weight>

    <weight> ::= <NON_NEG_FLOAT>
               | <NON_NEG_INTEGER>

    <literal> ::= <STRING_LITERAL>
                | <NON_NEG_FLOAT>
                | <NON_NEG_INTEGER>
                | "-" <NON_NEG_FLOAT>
                | "-" <NON_NEG_INTEGER>





Terminal Tokens
=======================

Special Symbols
----------------

.. code-block:: text

    LPAREN      : \(
    RPAREN      : \)
    MINUS       : -
    COMMA       : ,
    COLON       : :
    LBRACE      : {
    RBRACE      : }

Logical Operators
------------------

.. code-block:: text

    KW_EQ       : ==
    KW_GT       : >
    KW_LT       : <
    KW_GE       : >=
    KW_LE       : <=
    KW_NE       : !=
    KW_IN       : in
    KW_NOT_IN   : not\s+in
    KW_NOT      : not

Reserved Keywords
------------------

.. code-block:: text

    KW_DEF          : def
    KW_SALT         : salt
    KW_SPLITTERS    : splitters
    KW_IF           : if
    KW_ELIF         : else\s*if
    KW_ELSE         : else
    KW_WEIGHTED     : weighted
    KW_RETURN       : return
    KW_AND          : and
    KW_OR           : or

Identifiers & Literals
-----------------------

.. code-block:: text

    ID              : [a-zA-Z_][a-zA-Z0-9_]*
    NON_NEG_FLOAT   : \d+\.\d+          → Converted to float
    NON_NEG_INTEGER : \d+               → Converted to int
    STRING_LITERAL  : \".*?\"|\'.*?\'    → Strips quotes

Comments
--------

.. code-block:: text

    Block Comments  : /* ... */         → Multi-line C-style comments
    Inline Comments : //.*              → Single line comments (ignored)

Ignored Patterns
-----------------

.. code-block:: text

    Newlines       : \n+               → Updates line counter
    Whitespace     : \s+               → Ignored

Token Flow Diagram
-------------------

::

    Input Stream
         ↓
    +----------------+
    |  Ignore Rules  |
    | (WS, Comments) |
    +----------------+
         ↓
    +----------------+     +-----------------+
    | Token Matching |     | Special States  |
    | (Regex Rules)  |<--->| (BlockComment) |
    +----------------+     +-----------------+
         ↓
    +----------------+
    | Value Convert  |
    | (Numbers, Str) |
    +----------------+
         ↓
    Token Stream

Pattern Precedence
----------------

1. Block comments (special state)
2. Inline comments (ignored)
3. Whitespace (ignored)
4. Special symbols
5. Multi-character operators
6. Keywords
7. Literals (float, integer, string)
8. Identifiers

Error Handling
-------------

- Illegal characters trigger error() method
- Line numbers tracked for error reporting
- Block comments maintain separate lexer state

Notes
-----

1. All numeric literals must be non-negative (minus sign handled separately)
2. String literals support both single and double quotes
3. Keywords are case-sensitive
4. Block comments support nesting through state management
5. Whitespace is significant for some operators (e.g., 'not in')
