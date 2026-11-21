from tests.helpers.chem_helpers import generate_react_prod_atoms

from support.chem_types import *


import driver
from src.elements import get_all_atoms
from src.solver import balance_equation
from src.solver import make_system_of_equations
ref_solve_make_system_of_equations = driver.driver_import_reference('solver.make_system_of_equations')


from tests.helpers.naming import apply_names

import pytest

@pytest.mark.parametrize('react, prod, atoms', apply_names('make_system_of_equations', [True, True, True], [generate_react_prod_atoms(seed) for seed in range(50)], noparens=""))
def test_make_system_of_equations(react: Side, prod: Side, atoms: list[Element]):
    correct = ref_solve_make_system_of_equations(react, prod, atoms)
    out = make_system_of_equations(react, prod, atoms)
    assert correct == out
