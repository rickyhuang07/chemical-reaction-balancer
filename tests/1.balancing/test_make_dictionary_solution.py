from tests.helpers.equations import CHEMICAL_EQUATIONS
from tests.helpers.chem_helpers import generate_solution_eqn

from support.chem_types import *
from support.matrix import RationalVector

from src.solver import make_dictionary_solution

import driver
ref_solve_make_dictionary_solution = driver.driver_import_reference('solver.make_dictionary_solution')
ref_balance_equation = driver.driver_import_reference('solver.balance_equation')
ref_get_all_atoms = driver.driver_import_reference('elements.get_all_atoms')
ref_make_atom_vector = driver.driver_import_reference('solver.make_atom_vector')

from tests.helpers.naming import apply_names

import pytest


@pytest.mark.parametrize('solution, eq', apply_names('make_dictionary_solution', [True, True],  [generate_solution_eqn(seed) for seed in range(50)], noparens=""))
def test_make_dictionary_solution(solution: RationalVector, eq: str):
    correct = ref_solve_make_dictionary_solution(solution, eq)
    out = make_dictionary_solution(solution, eq)
    assert correct == out
