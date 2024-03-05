import operator

from sly import Parser

from pyab_tester.data_structures.syntax_tree import (
    ExperimentAST,
    ExperimentConditional,
    ExperimentGroup,
    Identifier,
    RecursivePredicate,
    TerminalPredicate,
)
from pyab_tester.language.lexer import ExperimentLexer


class ExperimentParser(Parser):
    tokens = ExperimentLexer.tokens

    precedence = (
        ("left", OR),
        ("left", AND),
        ("left", NOT),
    )

    @_("header_id opt_header_salt opt_splitter conditional")
    def header(self, p):
        return ExperimentAST(
            id=p.header_id,
            splitting_fields=p.opt_splitter,
            salt=p.opt_header_salt,
            conditions=p.conditional,
        )

    # *********** HEADER FIELDS *****************
    @_("")
    def empty(self, p):
        pass

    @_("DEF ID COLON")
    def header_id(self, p):
        return p.ID

    @_("empty")
    def opt_header_salt(self, p):
        return None

    @_("SALT COLON STRING_LITERAL")
    def opt_header_salt(self, p):
        return p.STRING_LITERAL

    @_("empty")
    def opt_splitter(self, p):
        return None

    @_("SPLITTERS COLON fields")
    def opt_splitter(self, p):
        return p.fields

    @_("ID COMMA fields")
    def fields(self, p):
        return [p.ID] + p.fields

    @_("ID")
    def fields(self, p):
        return [p.ID]

    # *************** Conditional rules *******************************
    @_("IF predicate LBRACE conditional RBRACE subconditional ")
    def conditional(self, p):
        return ExperimentConditional(
            predicate=p.predicate,
            true_branch=p.conditional,
            false_branch=p.subconditional,
        )

    @_("return_expr")
    def conditional(self, p):
        # "unconditioned" conditional. serves as a stop recursion rule
        return p.return_expr

    @_("ELIF predicate LBRACE conditional RBRACE subconditional")
    def subconditional(self, p):
        return ExperimentConditional(
            predicate=p.predicate,
            true_branch=p.conditional,
            false_branch=p.subconditional,
        )

    @_("ELSE LBRACE conditional RBRACE")
    def subconditional(self, p):
        return p.conditional

    @_("empty")
    def subconditional(self, p):
        return None

    # ************** predicates ****************
    @_("term logical_op term")
    def predicate(self, p):
        return TerminalPredicate(
            left_term=p.term0, logical_operator=p.logical_op, right_term=p.term1
        )

    @_("LPAREN predicate RPAREN")
    def predicate(self, p):
        return p.predicate

    @_("predicate AND predicate")
    def predicate(self, p):
        return RecursivePredicate(
            left_predicate=p.predicate0,
            boolean_operator=operator.and_,
            right_predicate=p.predicate1,
        )

    @_("predicate OR predicate")
    def predicate(self, p):
        return RecursivePredicate(
            left_predicate=p.predicate0,
            boolean_operator=operator.or_,
            right_predicate=p.predicate1,
        )

    @_("NOT predicate")
    def predicate(self, p):
        return RecursivePredicate(
            left_predicate=p.predicate,
            boolean_operator=operator.not_,
            right_predicate=None,
        )

    @_("literal")
    def term(self, p):
        return p.literal

    @_("ID")
    def term(self, p):
        return Identifier(name=p.ID)

    @_("tuple")
    def term(self, p):
        return p.tuple

    @_("LPAREN term op_term")
    def tuple(self, p):
        return [p.term] + p.op_term

    @_("COMMA term op_term")
    def op_term(self, p):
        return [p.term] + p.op_term

    @_("RPAREN")
    def op_term(self, p):
        return []

    # ********** Boolean ops*********************

    @_("LT")
    def logical_op(self, p):
        return operator.lt

    @_("GT")
    def logical_op(self, p):
        return operator.gt

    @_("GE")
    def logical_op(self, p):
        return operator.ge

    @_("LE")
    def logical_op(self, p):
        return operator.le

    @_("IN")
    def logical_op(self, p):
        return operator_in

    @_("NE")
    def logical_op(self, p):
        return operator.ne

    @_("EQ")
    def logical_op(self, p):
        return operator.eq

    @_("NOT_IN")
    def logical_op(self, p):
        return operator_not_in

    # *********** RETURN STATEMENTS *****************
    @_("RETURN return_statement")
    def return_expr(self, p):
        return p.return_statement

    @_("literal WEIGHTED weight")
    def return_statement(self, p):
        return [ExperimentGroup(group_definition=p.literal, group_weight=p.weight)]

    @_("literal WEIGHTED weight COMMA return_statement")
    def return_statement(self, p):
        return [
            ExperimentGroup(group_definition=p.literal, group_weight=p.weight)
        ] + p.return_statement

    # weights
    @_("NON_NEG_INTEGER")
    def weight(self, p):
        return p.NON_NEG_INTEGER

    @_("NON_NEG_FLOAT")
    def weight(self, p):
        return p.NON_NEG_FLOAT

    # ***************** literals ************************
    @_("MINUS NON_NEG_INTEGER")
    def literal(self, p):
        return -p.NON_NEG_INTEGER

    @_("MINUS NON_NEG_FLOAT")
    def literal(self, p):
        return -p.NON_NEG_FLOAT

    @_("NON_NEG_INTEGER")
    def literal(self, p):
        return p.NON_NEG_INTEGER

    @_("NON_NEG_FLOAT")
    def literal(self, p):
        return p.NON_NEG_FLOAT

    @_("STRING_LITERAL")
    def literal(self, p):
        return p.STRING_LITERAL
