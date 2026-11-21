import pytest
from fractions import Fraction
from support.matrix import MutableRationalMatrix2D
from tests.helpers.naming import apply_names
from tests.helpers.matrix_helpers import generate_random_pivot_matrices
from driver import driver_import_reference

ref_pivot_matrix = driver_import_reference('matrix_operations.pivot_matrix')

from src.matrix_operations import pivot_matrix


_SMALL_PIVOTS = [
    [[1, 2, 3, 4],
     [9, 8, 7, 6],
     [7, 3, 4, 8],
     ],
    [[1, 2, 3, 4, 5],
     [3, 2, 8, 6, 1],
     [5, 7, 3, 2, 1],
     [8, 2, 6, 4, 3],
     ],
    [[1, 2, 3, 4, 5, 6],
     [8, 2, 8, 3, 6, 2],
     [9, 4, 3, 7, 6, 3],
     [0, 0, 0, 0, 0, 0],
     [1, 2, 3, 4, 5, 6],
     ]
]


def _generate_small_pivot_matrices():
    matrices = []
    for arr in _SMALL_PIVOTS:
        mat = MutableRationalMatrix2D((len(arr), len(arr[0])))
        for i in range(mat.dimensions[0]):
            for j in range(mat.dimensions[1]):
                mat[i][j] = Fraction(arr[i][j])
        matrices.append([mat])
    return matrices


@pytest.mark.parametrize('matrix', apply_names('pivot_matrix', [False], _generate_small_pivot_matrices()))
def test_pivot_matrix_small(matrix: MutableRationalMatrix2D):
    for col in range(2, len(matrix)):
        correct = ref_pivot_matrix(matrix.mutable(), col)
        out = pivot_matrix(matrix, col)
        assert correct == out


@pytest.mark.parametrize('matrix', apply_names('pivot_matrix', [False], generate_random_pivot_matrices()))
def test_pivot_matrix_large(matrix: MutableRationalMatrix2D):
    for col in range(2, len(matrix)):
        correct = ref_pivot_matrix(matrix.mutable(), col)
        out = pivot_matrix(matrix, col)
        assert correct == out
