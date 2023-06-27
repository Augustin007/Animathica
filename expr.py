from typing import Any
from dataclasses import dataclass
from types import FunctionType

expression = tuple[str, tuple[Any, ...]]

equality = tuple[expression, expression]

@dataclass(eq=False, hash=False, frozen=True)
class expression_wrapper:
    expr:expression

    def __str__(self):
        return stringify(expr)

    __repr__ = __str__

class math_namespace(dict): # I have some plans for this, not implimented yet.
    pass

@dataclass(frozen=True)
class math_symbol:
    symbol: str
    num_args:int
    compute:FunctionType
    namespace:math_namespace
    strepr:str
    latex:str
    definition:tuple[equality,...]
    rules:tuple[equality, ...]

    def __post_init__(self):
        self.namespace[self.symbol]=self

def stringify(expr):
    return NotImplemented
    #return string version according to strepr

def apply(equa, expr):
    return NotImplemented
#return an application of a rule to an expression

def compute(expr):
    return NotImplemented


