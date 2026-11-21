from tests.helpers.chem_helpers import generate_side_atoms

from support.chem_types import *

import driver
ref_solve_make_compound_matrix = driver.driver_import_reference('solver.make_compound_matrix')

from src.solver import make_compound_matrix

from tests.helpers.naming import apply_names

import pytest


@pytest.mark.parametrize('side, atoms', apply_names('make_compound_matrix', [True, True], [generate_side_atoms(seed) for seed in range(50)], noparens=""))
def test_make_compound_matrix(side: Side, atoms: list[Element]):
    correct = ref_solve_make_compound_matrix(side, atoms)
    out = make_compound_matrix(side, atoms)
    assert correct == out
