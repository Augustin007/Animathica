'''
Simple simplifier
'''
from typing import TypeVar
from abc import abstractmethod

class CAS:
    '''Parent class for simple CAS'''
    pass

class CAS_type:
    constructors: list
    cases: set
    Type: tuple|type

    @abstractmethod
    def compute(self, at, to):
        pass


A = TypeVar('A')
B = TypeVar('B')
a = TypeVar('a')
b = TypeVar('b')
class CAS_function(CAS_type):
    function : dict
    Type : tuple
    constructors:list = []
    cases:set = set()

    @classmethod
    def match_constructor(cls, a):
        return None

    def __init__(self, Type, function):
        self.Type = (type(self), Type)
        self.function = function
        self.check_types()

    def __call__(self, a):
        if not guard(a.Type, self.in_type):
            raise TypeError(f'Invalid {a} for type {self.in_type}')
        for key, value in self.function.items():
            if not pattern_match(key, a): continue
            return (self.Type[1][1], value, key, a)
        raise ValueError(f'No match for {a}')

    @abstractmethod
    def check_types(self):
        pass

    def compute(self, at, to):
        pass # b.compute(at)

class CAS_independent_function(CAS_function):
    @property
    def in_type(self):
        return self.Type[1][0]
    @property
    def out_type(self):
        return self.Type[1][1]
    def check_types(self):
        in_type, out_type = self.Type[1]
        constructors = []
        cases = []
        generic_case = False
        for a, b in self.function.items():
            if (constructor:=in_type.match_constructor(a)):
                constructors.append(constructor)
            elif guard(infer_type(a), in_type):
                cases.append(a)
            elif is_generic_case(a):
                generic_case = True
            else:
                raise TypeError(f'{a} is not validly typed for {in_type}')
            if guard(infer_type(b), out_type):
                continue
            raise TypeError(f'{b} is not validly typed for {out_type}')
        if generic_case:
            return
        check_constructors(in_type, constructors, set(cases))
class Var(CAS_type):
    constructors = []
    cases = set()
    @classmethod
    def match_constructor(cls, a):
        return None
    def __init__(self, Type):
        self.Type = Type
    def compute(self, at, to):
        if at is self:
            return to
        return self
    
class CAS_dependent_function(CAS_function):
    @property
    def in_type(self):
        return self.Type[1].in_type

    def check_types(self):
        in_type = self.Type[1].in_type
        out_type = self.Type[1]
        constructors = []
        cases = []
        generic_case = False
        for a, b in self.function.items():
            if (constructor:=in_type.match_constructor(a)):
                constructors.append(constructor)
            elif guard(infer_type(a), in_type):
                cases.append(a)
            elif is_generic_case(a):
                generic_case=True
            else:
                raise TypeError(f'{a} is not validly typed for {in_type}')
            if guard(infer_type(b), out_type(a)):
                continue
            raise TypeError('{b} is not validly typed for {out_type}')
        if generic_case:
            return
        check_constructors(in_type, constructors, set(cases))

def guard(a, b) -> bool:
    if type(a) is tuple:
        if a[0]==b:
            return True
    return a==b

def is_generic_case(a):
    print('Hello')
    return True

# Lazy-computed thing
# (Type (infered on creation?), Value, at, to)

def infer_type(a: A):
    if type(a) is tuple:
        return a[0]
    if type(a) is Var:
        return a.Type
    return type(a)

def pattern_match(a, b):
    return True

def check_constructors(Type: CAS_type, constructors, cases: set)->bool:
    for constructor in Type.constructors:
        if constructor not in constructor and constructor.cases and ((constructor.cases & cases) != constructor.cases):
            raise TypeError(f'Missing constructor {constructor} for {Type}')
    for case in Type.cases:
        if case not in cases:
            raise TypeError(f'Missing case {case} for {Type}')
    return True

def compute(a):
    if type(a) is tuple:
        assert len(a)==4
        val = a[1].compute(*a[2:])
        if not guard(val.Type, a[0]):
            raise TypeError('Something went horribly wrong')
        return val
    return a
        
