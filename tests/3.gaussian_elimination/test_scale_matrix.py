import pytest
from support.matrix import MutableRationalMatrix2D
from tests.helpers.naming import apply_names
from tests.helpers.matrix_helpers import generate_random_matrix
from driver import driver_import_reference

ref_scale_matrix = driver_import_reference('matrix_operations.scale_matrix')

from src.matrix_operations import scale_matrix


@pytest.mark.parametrize('matrix', apply_names('scale_matrix', [False], [[generate_random_matrix(seed, 10, 10)] for seed in range(10, 50)]))
def test_scale_matrix(matrix: MutableRationalMatrix2D):
    for k in range(len(matrix)):
        correct = ref_scale_matrix(matrix.mutable(), k)
        out = scale_matrix(matrix.mutable(), k)
        assert correct == out
