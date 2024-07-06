from typing import TypeVar
from types import Callable

class expression:
    pass

class magma(expression):
    compute: FunctionType[[A,A], A]
    abelian: bool

class quasigroup(magma):
    divisibility: FunctionType[[A,A], A]

class unital_magma(magma):
    identity: A

class semigroup(magma):
    pass

class loop(quasigroup,unital_magma):
    pass

class associative_quasigroup(quasigroup,semigroup):
    pass

class monoid(unital_magma, semigroup):
    pass

class group(monoid, associative_quasigroup,loop):
    pass


class abelian_group(expression):
    pass

class ring_lower(abelian_group):
    pass

