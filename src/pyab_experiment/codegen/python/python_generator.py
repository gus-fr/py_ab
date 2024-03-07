"""Module that does the translation from an AST to a python function"""
from pyab_experiment.language.grammar import (
    BooleanOperatorEnum,
    ConditionalType,
    ExperimentAST,
    ExperimentConditional,
    ExperimentGroup,
    Identifier,
    LogicalOperatorEnum,
    RecursivePredicate,
    TerminalPredicate,
)


class PythonCodeGen:
    """class that holds intermediate state (e.g indentation level, variable names)
    while generating code
    """

    def __init__(self, experiment_ast: ExperimentAST, indentation_char: str = "\t"):
        self._experiment_ast = experiment_ast
        self._local_vars = set()
        self._conditional_ids = set()  # to save conditional variables seen
        self._indentation_char = indentation_char
        self._newline = "\n"
        self._indent_depth = 0

    @property
    def local_vars(self):
        return sorted(self._local_vars)

    @property
    def conditional_ids(self):
        return sorted(self._conditional_ids)

    def render_topline(self) -> str:
        """imports et.al"""
        return (
            f"from functools import partial{self._newline}"
            f"from pyab_experiment.binning.binning import deterministic_choice{self._newline}"
            f"{self._newline}#*******AUTOGENERATED DO NOT MODIFY ***********{self._newline}{self._newline}"
        )

    def indent(self) -> str:
        return "".join([self._indentation_char * self._indent_depth])

    def generate(self) -> str:
        """main method. Does a DFS on the syntax tree rendering code as it traverses the nodes"""
        self._indent_depth += 1
        salt_def = (
            f"'{self._experiment_ast.salt}'"
            if self._experiment_ast.salt is not None
            else "''"
        )
        fields_def = ""
        if self._experiment_ast.splitting_fields:
            for var in self._experiment_ast.splitting_fields:
                self._local_vars.add(var)
            fields_def = f"''.join([{', '.join(self.local_vars)}])"

        if len(fields_def) == 0:
            composite_key = "None"
        else:
            composite_key = f"{salt_def}+{fields_def}"

        # generate conditional defn
        variant_fn_body = self._generate_conditionals(self._experiment_ast.conditions)
        variant_fn_signature = f"def choose_experiment_variant({', '.join(self.conditional_ids)}):{self._newline}"
        variable_assignment = ", ".join([f"{id}={id}" for id in self.conditional_ids])
        function_call = f"{self.indent()}return choose_experiment_variant({variable_assignment})({composite_key}){self._newline}"

        fn_defn = f"def {self._experiment_ast.id}({', '.join(self.local_vars+self.conditional_ids)}):{self._newline}"
        return f"{self.render_topline()}{fn_defn}{function_call}{variant_fn_signature}{variant_fn_body}"

    def _generate_conditionals(
        self, condition: ExperimentConditional | list[ExperimentGroup]
    ) -> str:
        """generates the (possibly nested) conditional statements, and their return functions
        goes through through all the contitionals and rendering
        appropriate function definitions
        """
        match condition:
            case ExperimentConditional():
                predicate = self._generate_predicate(condition.predicate)
                self._indent_depth += 1
                true_branch_stmt = self._generate_conditionals(condition.true_branch)
                self._indent_depth -= 1
                false_branch_stmt = (
                    self._generate_conditionals(condition.false_branch)
                    if condition.false_branch is not None
                    else ""
                )
                match condition.conditional_type:
                    case ConditionalType.IF:
                        return f"{self.indent()}if {predicate}:{self._newline}{true_branch_stmt}{false_branch_stmt}"
                    case ConditionalType.ELIF:
                        return f"{self.indent()}elif {predicate}:{self._newline}{true_branch_stmt}{false_branch_stmt}"
                    case ConditionalType.ELSE:
                        return f"{self.indent()}else:{self._newline}{true_branch_stmt}{false_branch_stmt}"

            case [*_]:
                statement = self._generate_group_return_statement(condition)
                return statement

            case _:
                raise RuntimeError(
                    f"wrong type passed to conditional gen {type(condition)}"
                )

    def _generate_predicate(
        self, predicate: TerminalPredicate | RecursivePredicate | None
    ) -> str:
        match predicate:
            case TerminalPredicate():
                l_term = self._generate_term(predicate.left_term)
                r_term = self._generate_term(predicate.right_term)
                operator = self._generate_op(predicate.logical_operator)

                return f"({l_term} {operator} {r_term})"
            case RecursivePredicate():
                l_pred = self._generate_predicate(predicate.left_predicate)
                r_pred = self._generate_predicate(predicate.right_predicate)
                operator = self._generate_op(predicate.boolean_operator)
                if (
                    predicate.boolean_operator == BooleanOperatorEnum.NOT
                ):  # special case
                    return f"({operator} {l_pred})"

                return f"({l_pred} {operator} {r_pred})"
            case None:
                return ""
            case _:
                raise RuntimeError(
                    f"wrong type passed to predicate gen {type(predicate)}"
                )

    def _generate_term(self, term: float | int | str | tuple | Identifier) -> str:
        match term:
            case Identifier(name=identifier_name):
                self._conditional_ids.add(identifier_name)
                return identifier_name
            case str():
                return f"'{term}'"
            case _:
                return term

    def _generate_op(self, op: LogicalOperatorEnum | BooleanOperatorEnum) -> str:
        match op:
            case LogicalOperatorEnum.EQ:
                return "=="
            case LogicalOperatorEnum.NE:
                return "!="
            case LogicalOperatorEnum.GT:
                return ">"
            case LogicalOperatorEnum.GE:
                return ">="
            case LogicalOperatorEnum.LT:
                return "<"
            case LogicalOperatorEnum.LE:
                return "<="
            case LogicalOperatorEnum.NOT_IN:
                return "not in"
            case LogicalOperatorEnum.IN:
                return "in"
            case BooleanOperatorEnum.NOT:
                return "not"
            case BooleanOperatorEnum.AND:
                return "and"
            case BooleanOperatorEnum.OR:
                return "or"
            case _:
                raise RuntimeError(f"OperatorEnum not matched: {op}")

    def _generate_group_return_statement(
        self, group_statement: list[ExperimentGroup]
    ) -> str:
        """unwrap the experiment group, into a partial function call that applies the splitter logic"""

        population_list = str([group.group_definition for group in group_statement])
        weight_list = str([group.group_weight for group in group_statement])
        return f"{self.indent()}return partial(deterministic_choice,population={population_list},weights={weight_list}){self._newline}"
