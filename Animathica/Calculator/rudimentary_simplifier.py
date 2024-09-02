from typing import Callable, Any
from numbers import Number
from fractions import Fraction
from operator import add, mul, call
from abc import abstractmethod
from ..logger import log, log_function, log_class, logging, log_skip, log_flags

@log_class(logging.DEBUG)
class expression:
    __radd__ = __add__ = lambda self, other: addition(self, other)
    __sub__ = lambda self, other: addition(self, multiplication(other, -1))
    __rsub__ = lambda self, other: addition(multiplication(self, -1), other)
    __rmul__ = __mul__ = lambda self, other: multiplication(self, other)
    __truediv__ = lambda self, other: multiplication(self, exponentiation(other,-1))
    __rtrudediv__ = lambda self, other: multiplication(exponentiation(self, -1), other)
    __pow__ = lambda self, other: exponentiation(self, other)
    __rpow__ = lambda self, other: exponentiation(other, self)
    __neg__ = lambda self: multiplication(self, -1)
    def simplify(self):
        return self
    def on_simplify(self):
        return self

@log_function(logging.DEBUG)
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

@log_class(logging.DEBUG)
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
        sa = self.a.simplify()
        sb = self.b.simplify()
        if hasattr(self, 'identity'):
            if sa.__simplified_eq__(self.identity):
                return sb
            if sb.__simplified_eq__(self.identity):
                return sa
        if isinstance(sa, number) and isinstance(sb, number):
            return number(self.compute(sa.value, sb.value))
        return type(self)(sa, sb).on_simplify()
        #return self.on_simplify()

    def on_simplify(self)->expression:
        return self

    def __eq__(self, other):
        sself = self.simplify()
        sother = other.simplify()
        return sself.__simplified_eq__(sother)

    def __simplified_eq__(self, sother):
        if isinstance(sother, type(self)):
            return self.a == sother.a and self.b == sother.b
        return False

@log_class(logging.DEBUG)
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
        return self.__simplified_eq__(sother)

    def __simplified_eq__(self, sother):
        if type(sother) is number:
            return self.value == sother.value
        return False

@log_class(logging.DEBUG)
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
        return self.__simplified_eq__(sother)
    
    def __simplified_eq__(self, sother):
        if type(sother) is variable:
            return self.name == sother.name
        return False

@log_function(logging.DEBUG)
def flatten(this, over, that, pre_simplified=False):
    '''
    flattens an expression like (1+(1+1)) into an element of type that, flattening out over 'over' (+) to get (1+1+1)
    '''
    if isinstance(this, over):
        return (*flatten(this.a, over, that), *flatten(this.b, over, that))
    if isinstance(this, that):
        if pre_simplified:
            return this.items
        return (*this.simplify().items,)
    if pre_simplified:
        return (this,)
    return (this.simplify(),)
variables: dict[str, variable] = {}

@log_class(logging.DEBUG)
class semiring(expression):
    inner: Any
    outer: Any
    items: tuple[expression, ...]
    def __init__(self, *items, pre_simplified=False):
        #for item in items:
        #    assert isinstance(item, self.inner)
        self.items = items
        self.pre_simplified = pre_simplified
        # self.items = flatten(item, self.inner)
        self.on_init()

    def on_init(self):
        return self

    def simplify(self)->expression:
        items:list = []
        for item in self.items:
            if self.pre_simplified:
                items.extend(map(self.split, flatten(item, self.inner, type(self), True)))
                continue
            items.extend(map(self.split, flatten(item.simplify(), self.inner, type(self))))
        log(logging.INFO, f'Item count for {self.__class__}: {items}')
        constant = self.inner.identity
        new: list = []
        while items:
            log(logging.INFO, f'While Loop, current item count {items}')
            numb, expression = items.pop()
            log(logging.INFO, f'Current expression {expression}')
            if isinstance(expression, number):
                constant = self.inner.compute(constant, expression)
                continue
            index = 0
            for num, expr in items.copy():
                log(logging.INFO, f'For loop, current item count {items}')
                log(logging.INFO, f'Matching {expression} against {expr}')
                log(logging.INFO, f'Matching {type(expression)} with {type(expr)}')
                log(logging.INFO, f'{expr==expression}')
                if expr == expression:
                    log(logging.INFO, f'Matched {expression} with {expr}')
                    items.pop(index)
                    numb += num
                    log(logging.INFO, f'Total = {numb}')
                    continue
                index += 1
            log(logging.INFO, f'{expression}, {numb}')
            numb = numb.simplify()
            #if hasattr(self.inner, 'identity') and self.inner.identity.__simplified_eq__(numb):
            #    continue
            new.append(self.outer(expression, numb).simplify())
        if constant != self.inner.identity:
            new.append(constant.simplify())
        if len(new) == 0:
            return self.inner.identity
        if len(new) == 1:
            return new[0]
        return self.__class__(*new)

    @abstractmethod
    def split(self, item):
        pass

    def __eq__(self, other):
        a = self.simplify()
        b = other.simplify()
        return a.__simplified_eq__(b)

    def __simplified_eq__(self, other):
        if type(other) != type(self):
            return False
        for item in self.items:
            if item not in other.items:
                return False
            return True
        return False

    def __repr__(self):
        return self.inner.infix.join(map(repr, self.items))

class addition(binary_operation):
    compute = add
    infix = '+'
    identity = number(0)

    @log_function(logging.DEBUG)
    def on_simplify(self):
        return add_mul(self.a, self.b, pre_simplified=True).simplify()

class multiplication(binary_operation):
    compute = mul
    infix = '*'
    identity = number(1)

    @log_function(logging.DEBUG)
    def on_simplify(self):
        if addition.identity in (self.a, self.b):
            return addition.identity
        return mul_pow(self.a, self.b, pre_simplified=True).simplify()

@log_class(logging.DEBUG)
class exponentiation(binary_operation):
    compute = pow
    infix = '**'
    def on_simplify(self):
        if self.b == number(1):
            return self.a
        return self

@log_class(logging.DEBUG)
class nest(binary_operation):
    compute = call
    infix = ''
    def on_init(self):
        assert isinstance(self.a, function)

@log_class(logging.DEBUG)
class function:
    def __init__(self, func, safe_func):
        self.func = func
    def __call__(self, *args):
        return nest(self, args)
    def __repr__(self):
        return self.func.__name__

@log_class(logging.DEBUG)
class add_mul(semiring):
    inner = addition
    outer = multiplication
    def split(self, item):
        if isinstance(item, mul_pow):
            if isinstance(item.items[-1], number):
                return item.items[-1], mul_pow(*item.items[:-1])
        return number(1), item

@log_class(logging.DEBUG)
class mul_pow(semiring):
    inner = multiplication
    outer = exponentiation

    def split(self, item):
        if isinstance(item, exponentiation):
            return item.b, item.a
        return number(1), item

#log_flags['simplify'] = logging.INFO
