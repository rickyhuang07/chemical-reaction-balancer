
from support.parser import parse_equation
from support.chem_types import Solution

from tests.helpers.balance import check_is_balanced
from tests.helpers.equations import CHEMICAL_EQUATIONS

from src.solver import balance_equation


def print_equation(eqn: str):
    reacts, prods = parse_equation(eqn, False)
    solution: Solution = balance_equation(eqn)
    react_str: str = " + ".join([(str(solution[x])
                                if solution[x] != 1 else "") + x for x in reacts])
    prod_str: str = " + ".join([(str(solution[x]) if solution[x] !=
                                 1 else "") + x for x in prods])
    print(react_str + " \u2192 " + prod_str)


for e in CHEMICAL_EQUATIONS:
    solution: Solution = balance_equation(e)
    print(solution)
    print_equation(e)
    check_is_balanced(e, solution)
