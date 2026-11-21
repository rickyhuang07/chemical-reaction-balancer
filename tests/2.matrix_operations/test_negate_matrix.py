import pytest
from support.matrix import MutableRationalMatrix2D, RationalMatrix2D
from tests.helpers.naming import apply_names
from tests.helpers.matrix_helpers import generate_random_matrix
from driver import driver_import_reference

ref_negate_matrix = driver_import_reference('matrix_operations.negate_matrix')

from src.matrix_operations import negate_matrix


@pytest.mark.parametrize('matrix', apply_names('negate_matrix', [False], [[generate_random_matrix(seed)] for seed in range(10, 50)]))
def test_negate_matrix(matrix: RationalMatrix2D):
    orig: MutableRationalMatrix2D = matrix
    negated: MutableRationalMatrix2D = negate_matrix(orig.mutable())
    double_negated: RationalMatrix2D = negate_matrix(negated.mutable())

    assert orig is not negated, "Make sure you construct a *new* matrix to negate. Do not edit the old one!"
    assert orig != negated, "You may have forgotten to negate your matrix!"
    assert orig == double_negated, f"Your matrix is {matrix}, but if we double negate your matrix, it gives {double_negated}."

    assert (orig + negated) == RationalMatrix2D(orig.dimensions), f"Your matrix, {orig}, added to its negation, {negated}, is not the zero matrix."
