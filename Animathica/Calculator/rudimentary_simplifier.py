from typing import Callable, Any
from numbers import Number
from fractions import Fraction
from operator import add, mul, call
from abc import abstractmethod
from ..logger import log, log_function, log_class, logging, log_skip

@log_class(logging.INFO)
class expression:
    __radd__ = __add__ = lambda self, other: addition(self, other)
    __sub__ = lambda self, other: addition(self, multiplication(other, -1))
    __rsub__ = lambda self, other: addition(multiplication(self, -1), other)
    __rmul__ = __mul__ = lambda self, other: multiplication(self, other)
    __truediv__ = lambda self, other: multiplication(self, exponentiation(other,-1))
    __rtrudediv__ = lambda self, other: multiplication(exponentiation(self, -1), other)
    __pow__ = lambda self, other: exponentiation(self, other)
    __rpow__ = lambda self, other: exponentiation(other, self)
    def simplify(self):
        return self
    def on_simplify(self):
        return self

@log_function(logging.INFO)
def safe(*element):
    if len(element) != 1:
        return map(safe, element)
    a = element[0]
    if isinstance(a, Number):
        return number(a)
    if isinstance(a, expression):
        return a
    if isinstance(a, str):
        return variable(a)
    return a

@log_class(logging.INFO)
class binary_operation(expression):
    a: expression
    b: expression
    infix: str
    compute: Callable


    def __init__(self, a, b):
        self.a = safe(a)
        self.b = safe(b)
        self.on_init()
    
    def on_init(self):
        pass
    
    def __repr__(self):
        return f'({self.a}{self.infix}{self.b})'

    def simplify(self)->expression:
        if hasattr(self, 'identity'):
            if self.a == self.identity:
                return self.b
            if self.b == self.identity:
                return self.a
        if isinstance(self.a, number) and isinstance(self.b, number):
            return number(self.compute(self.a.value, self.b.value))
        return self.on_simplify()

    def on_simplify(self)->expression:
        return self

    def __eq__(self, other):
        sself = self.simplify()
        sother = other.simplify()
        if type(sself) == type(self):
            if type(sother) == type(sself):
                return sself.a == sother.a and sself.b == sother.b
            return False
        return sself == sother

@log_class(logging.INFO)
class number(expression):
    def __init__(self, value):
        if int(value) == value:
            self.value = int(value)
            return
        self.value = Fraction(value)
    value: int|Fraction

    def __repr__(self):
        return repr(self.value)

    def __eq__(self, other):
        sother = other.simplify()
        if type(sother) is number:
            return self.value == sother.value
        return False

@log_class(logging.INFO)
class variable(expression):
    name: str
    constant: bool
    value: None|Number
    def __init__(self, name:str, constant=False, value=None):
        if name in variables:
            other = variables[name]
            assert constant==other.constant
            assert value==other.value
        self.name = name
        self.constant = constant
        self.value = value
        variables[name] = self

    def __repr__(self):
        return self.name
        #return f'variable({repr(self.name)})'

    def __eq__(self, other):
        sother = other.simplify()
        if type(sother) is variable:
            return self.name == sother.name
        return False

@log_function(logging.INFO)
def flatten(this, over, that):
    if isinstance(this, over):
        return (*flatten(this.a, over, that), *flatten(this.b, over, that))
    if isinstance(this, that):
        return (*this.simplify().items,)
    return (this.simplify(),)
variables: dict[str, variable] = {}

@log_class(logging.INFO)
class semiring(expression):
    inner: Any
    outer: Any
    items: tuple[expression, ...]
    def __init__(self, *items):
        #for item in items:
        #    assert isinstance(item, self.inner)
        self.items = items
        # self.items = flatten(item, self.inner)

    def simplify(self)->expression:
        if len(self.items) == 1:
            items = list(map(self.split, flatten(self.items[0], self.inner, type(self))))
        else: 
            items = list(map(self.split, self.items))
        constant = self.inner.identity
        new: list = []
        while items:
            numb, expression = items.pop()
            if isinstance(expression, number):
                constant = self.inner.compute(constant, expression)
                continue
            index = 0
            for num, expr in items.copy():
                if expr == expression:
                    items.pop(index)
                    numb += num
                    continue
                index += 1
            new.append(self.outer(expression, numb.simplify()).simplify())
        if constant!= self.inner.identity:
            new.append(constant.simplify())
        return self.__class__(*new)

    @abstractmethod
    def split(self, item):
        pass

    def __eq__(self, other):
        a = self.simplify()
        b = other.simplify()
        if type(a) == type(self):
            if type(other) == type(a):
                for item in self.items:
                    if item not in other.items:
                        return False
                return True
            return False
        return a == b

    def __repr__(self):
        return self.inner.infix.join(map(repr, self.items))

class addition(binary_operation):
    compute = add
    infix = '+'
    identity = number(0)

    @log_function(logging.INFO)
    def on_simplify(self):
        return add_mul(self).simplify()

class multiplication(binary_operation):
    compute = mul
    infix = '*'
    identity = number(1)

    @log_function(logging.INFO)
    def on_simplify(self):
        return mul_pow(self).simplify()

@log_class(logging.INFO)
class exponentiation(binary_operation):
    compute = pow
    infix = '**'
    def on_simplify(self):
        if self.b == number(1):
            return self.a

@log_class(logging.INFO)
class nest(binary_operation):
    compute = call
    infix = ''
    def on_init(self):
        assert isinstance(self.a, function)

@log_class(logging.INFO)
class function:
    def __init__(self, func, safe_func):
        self.func = func
    def __call__(self, *args):
        return nest(self, args)
    def __repr__(self):
        return self.func.__name__

@log_class(logging.INFO)
class add_mul(semiring):
    inner = addition
    outer = multiplication
    def split(self, item):
        if isinstance(item, mul_pow):
            if isinstance(item.items[-1], number):
                return item.items[-1], mul_pow(*item.items[:-1])
        return number(1), item

@log_class(logging.INFO)
class mul_pow(semiring):
    inner = multiplication
    outer = exponentiation

    def split(self, item):
        if isinstance(item, exponentiation):
            return item.b, item.a
        return number(1), item

