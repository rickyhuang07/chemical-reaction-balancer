from tests.helpers.balance import check_is_balanced
from tests.helpers.equations import CHEMICAL_EQUATIONS

from support.chem_types import *

from support.parser import parse_equation

from src.elements import get_all_atoms
from src.solver import balance_equation

from tests.helpers.naming import apply_names

import pytest

@pytest.mark.parametrize('eqn', apply_names('balance_equation', [True], [[eqn] for eqn in CHEMICAL_EQUATIONS]))
def test_check_balance_equation(eqn: str):
    solution: Solution = balance_equation(eqn)
    check_is_balanced(eqn, solution)
