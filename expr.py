from typing import Any
from dataclasses import dataclass
from types import FunctionType

expression = tuple[str, tuple[Any, ...]]

equality = tuple[expression, expression]

class math_namespace(dict): # I have some plans for this, not implimented yet.
    pass

@dataclass(eq=False, unsafe_hash=True, frozen=True)
class expression_wrapper:
    expr:expression
    namespace: math_namespace

    def __str__(self):
        return stringify(self.expr, self.namespace)

    __repr__ = __str__


@dataclass(frozen=True, slots=True)
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

    def __str__(self):
        return strepr

def stringify(expr, namespace):
    if not isinstance(expr, tuple):
        return str(expr)
    symbol = namespace[expr[0]]
    temp = symbol.strepr
    return _string_inc(temp, expr, lambda n: stringify(n, namespace))

def latexify(expr, namespace):
    if not isinstance(expr, tuple):
        return str(expr)
    symbol = namespace[expr[0]]
    temp = symbol.latex
    return _string_inc(temp, expr, lambda n: latexify(n, namespace))

def _string_inc(run, expr, function):
    for num, arg in enumerate(expr[1:]):
        run = run.replace(f'${num}$', function(arg))
    return run
#return string version according to strepr

def apply(equa, expr):
    return NotImplemented
#return an application of a rule to an expression

def compute(expr, namespace):
    if not isinstance(expr, tuple):
        return expr
    symbol = namespace[expr[0]]
    return symbol.compute(*(compute(a, namespace) for a in expr[1:]))

if __name__ == '__main__':
    mns = math_namespace()
    Plus = math_symbol('+', 2, lambda a,b:a+b, mns, '$0$+$1$', '{$0$}+{$1$}', (), ())
    # Test = expression_wrapper(('+', 1, ('+', 1, 2)), mns)
    # str(Test)
    # stringify(Test.expr, mns)
    # latexify(Test.expr, mns)
    # compute(Test.expr, mns)

