import pytest
from support.matrix import MutableRationalMatrix2D
from tests.helpers.naming import apply_names
from tests.helpers.matrix_helpers import generate_random_refable_matrices, refable_matrix_to_eq
from driver import driver_import_reference

ref_gaussian_elim = driver_import_reference('matrix_operations.gaussian_elimination')

from src.matrix_operations import gaussian_elimination as gaussian_elim


@pytest.mark.parametrize('matrix', apply_names('gaussian_elimination', [False], generate_random_refable_matrices(k=7)))
def test_gaussian_elimination(matrix: MutableRationalMatrix2D):
    A, b = refable_matrix_to_eq(matrix)
    correct = ref_gaussian_elim(A.mutable(), b.mutable())
    out = gaussian_elim(A.mutable(), b.mutable())
    assert correct == out
