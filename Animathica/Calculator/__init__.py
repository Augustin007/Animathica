'''
Quick explanation of files.

expr.py is the first file written for this whole project. While the ideas aren't still in use, there are still some bits of code I want to salvage from there.

simplifier.py is the incomplete simplifier.

rudimentary_simplifier.py is the temporary working simplifier.
'''
from .rudimentary_simplifier import *

x, y, z = safe(*'xyz')

def Calculator_Test():
    while (Special:=input()):
        try:
            Special = eval(Special)
            if isinstance(Special, expression):
                Special = Special.simplify()
            print(repr(Special))
        except Exception as e:
            print(e)
    return

