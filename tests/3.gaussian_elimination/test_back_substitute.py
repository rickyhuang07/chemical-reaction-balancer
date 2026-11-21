import pytest
from support.matrix import MutableRationalMatrix2D
from tests.helpers.naming import apply_names
from tests.helpers.matrix_helpers import generate_random_refable_matrices
from driver import driver_import_reference

ref_back_substitute = driver_import_reference('matrix_operations.back_substitute')

from src.matrix_operations import back_substitute


@pytest.mark.parametrize('matrix', apply_names('back_substitute', [False], generate_random_refable_matrices(k=7)))
def test_back_substitute(matrix: MutableRationalMatrix2D):
    correct = ref_back_substitute(matrix.mutable())
    out = back_substitute(matrix.mutable())
    assert correct == out
