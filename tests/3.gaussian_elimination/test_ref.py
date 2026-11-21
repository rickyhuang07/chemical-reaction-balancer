import pytest
from fractions import Fraction
from support.matrix import MutableRationalMatrix2D
from tests.helpers.naming import apply_names
from tests.helpers.matrix_helpers import generate_random_refable_matrices
from driver import driver_import_reference

ref_ref = driver_import_reference('matrix_operations.ref')

from src.matrix_operations import ref


def _generate_zero_row_matrix():
    SZ = 5
    mat = MutableRationalMatrix2D((SZ - 1, SZ))
    x = [
        [2, 4, 6, 8, 10, 4],
        [0] * SZ,
        [0] * SZ,
        [1, 2, 3, 4, 5, 2],
        [1, 2, 3, 4, 5, 2],
    ]

    for i in range(mat.dimensions[0]):
        for j in range(mat.dimensions[1]):
            mat[i][j] = Fraction(x[i][j])
    return mat


def test_ref_zero_row():
    with_multiple_zero_rows = _generate_zero_row_matrix()

    correct = ref_ref(with_multiple_zero_rows.mutable())
    try:
        out = ref(with_multiple_zero_rows.mutable())
    except ZeroDivisionError as e:
        raise ZeroDivisionError("Remember to remove any zero rows that appear in your matrix!") from e
    assert correct == out, "ref should work on matrices with zero rows"


@pytest.mark.parametrize('matrix', apply_names('ref', [False], generate_random_refable_matrices(k=7)))
def test_ref_large_matrix(matrix: MutableRationalMatrix2D):
    correct = ref_ref(matrix.mutable())
    out = ref(matrix.mutable())
    assert correct == out
