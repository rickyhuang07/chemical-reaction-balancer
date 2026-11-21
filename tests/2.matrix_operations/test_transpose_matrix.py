import pytest
from support.matrix import MutableRationalMatrix2D, RationalMatrix2D
from tests.helpers.naming import apply_names
from tests.helpers.matrix_helpers import generate_random_matrix
from driver import driver_import_reference

ref_transpose_matrix = driver_import_reference('matrix_operations.transpose_matrix')

from src.matrix_operations import transpose_matrix


@pytest.mark.parametrize('matrix', apply_names('transpose_matrix', [False], [[generate_random_matrix(seed)] for seed in range(10, 50)]))
def test_transpose_matrix(matrix: RationalMatrix2D):
    orig: MutableRationalMatrix2D = matrix
    transposed: RationalMatrix2D = transpose_matrix(orig.mutable())
    double_transposed: RationalMatrix2D = transpose_matrix(transposed.mutable())

    assert orig is not transposed, "Make sure you construct a *new* matrix to negate. Do not edit the old one!"

    assert orig.dimensions == (transposed.dimensions[1], transposed.dimensions[0]), f"The transposed matrix's dimensions are {transposed.dimensions}, and your original matrix's are {orig.dimensions}."

    assert orig == double_transposed, "If you transpose your matrix twice, it does not give the original."
    assert orig.dimensions == double_transposed.dimensions, "If you transpose your matrix twice, the dimensions no longer match up."

    for i in range(orig.dimensions[0]):
        for j in range(orig.dimensions[1]):
            assert (orig[i][j] == transposed[j][i]), f"Index ({i}, {j}) of the original is {orig[i][j]}, but index ({j}, {i}) of the transposed matrix is {transposed[j][i]}."
            assert (orig[i][j] == double_transposed[i][j]), "If you transpose your matrix twice, the individual elements no longer match up."
