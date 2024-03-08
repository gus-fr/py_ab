"""_summary_
Module that houses the abstract syntax tree (AST) representation of an experiment
It's a collection of pydantic classes that represent a tree with several specialized nodes
each representing a specific data structure of the experiment
"""

from enum import Enum, auto
from typing import Callable, Union

from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt


class LogicalOperatorEnum(Enum):
    EQ = auto()
    GT = auto()
    LT = auto()
    GE = auto()
    LE = auto()
    NE = auto()
    IN = auto()
    NOT_IN = auto()


class BooleanOperatorEnum(Enum):
    AND = auto()
    OR = auto()
    NOT = auto()


class ConditionalType(Enum):
    IF = auto()
    ELIF = auto()
    ELSE = auto()


class ExperimentGroup(BaseModel):
    group_definition: str
    group_weight: Union[NonNegativeFloat, NonNegativeInt]


class Identifier(BaseModel):
    name: str


class TerminalPredicate(BaseModel):
    left_term: Union[float, int, str, tuple, Identifier]
    logical_operator: LogicalOperatorEnum
    right_term: Union[float, int, str, tuple, Identifier]


class RecursivePredicate(BaseModel):
    left_predicate: Union[TerminalPredicate, "RecursivePredicate"]
    boolean_operator: BooleanOperatorEnum
    right_predicate: Union[TerminalPredicate, "RecursivePredicate", None]


class ExperimentConditional(BaseModel):
    conditional_type: ConditionalType
    predicate: Union[TerminalPredicate, RecursivePredicate, None]
    true_branch: Union[list[ExperimentGroup], "ExperimentConditional"]
    false_branch: Union[list[ExperimentGroup], "ExperimentConditional", None]


class ExperimentAST(BaseModel):
    id: str
    splitting_fields: list[str] | None
    salt: str | None
    conditions: Union[ExperimentConditional, list[ExperimentGroup]]
