from fractions import Fraction

from pandas import pivot

from driver import provide_reference_impl
from support.chem_types import *

from support.matrix import MutableRationalVector, RationalMatrix2D, MutableRationalMatrix2D, RationalVector
from support.parser import *


# See elements.py if you have questions about this line.
@provide_reference_impl
def negate_matrix(matrix: MutableRationalMatrix2D) -> MutableRationalMatrix2D:
    """
    Returns the negation of the given matrix.

    Parameters:
        matrix (MutableRationalMatrix2D): Matrix to be negated.

    Returns:
        MutableRationalMatrix2D: A matrix that represents negative one times
        the given matrix parameter.
    """
    rows = matrix.dimensions[0]
    cols = matrix.dimensions[1]
    res = MutableRationalMatrix2D(dimensions=(rows, cols))

    for i in range(rows):
        for j in range(cols):
            res[i][j] = -matrix[i][j]
    return res


@provide_reference_impl
def transpose_matrix(matrix: MutableRationalMatrix2D) -> MutableRationalMatrix2D:
    """
    Returns the transpose of the given matrix.

    Parameters:
        matrix (MutableRationalMatrix2D): Matrix to be transposed.

    Returns:
        MutableRationalMatrix2D: A matrix that represents the transpose
        of the given matrix parameter.
    """
    rows = matrix.dimensions[0]
    cols = matrix.dimensions[1]
    res = MutableRationalMatrix2D(dimensions=(cols, rows))
    for i in range(rows):
        for j in range(cols):
            res[j][i] = matrix[i][j]
    return res


@provide_reference_impl
def pivot_matrix(matrix: MutableRationalMatrix2D, k: int) -> MutableRationalMatrix2D:
    """
    Pivots the kth row of the given matrix.

    Parameters:
        matrix (MutableRationalMatrix2D): Matrix to pivot.
        k (int): Row number to pivot.

    Returns:
        MutableRationalMatrix2D: A matrix that represents the given matrix with
        the given row pivoted.
    """
    rows = matrix.dimensions[0]
    max_row = k
    for i in range(k + 1, rows):
        if abs(matrix[i][k]) > abs(matrix[max_row][k]):
            max_row = i
    return matrix.swap_rows(k, max_row).mutable()


@provide_reference_impl
def scale_matrix(matrix: MutableRationalMatrix2D, k: int) -> MutableRationalMatrix2D:
    """
    Scales the given matrix using column k.

    Parameters:
        matrix (MutableRationalMatrix2D): Matrix to scale.
        k (int): Row and column number to scale by.

    Returns:
        MutableRationalMatrix2D: A matrix that represents the given matrix scaled by
        the column k.
    """
    rows = matrix.dimensions[0]
    cols = matrix.dimensions[1]
    res = MutableRationalMatrix2D(dimensions=(rows, cols))
    for i in range(rows):
        for j in range(cols):
            res[i][j] = matrix[i][j]
    pivot = res[k][k]

    for j in range(cols):
        res[k][j] /= pivot
    for i in range(k + 1, rows):
        factor = res[i][k]
        for j in range(cols):
            res[i][j] -= factor * res[k][j]
    return res


@provide_reference_impl
def ref(matrix: MutableRationalMatrix2D) -> MutableRationalMatrix2D:
    """
    Performs elementary row operations on the given matrix to reach REF form.

    Parameters:
        matrix (MutableRationalMatrix2D): Matrix to put into REF form.

    Returns:
        MutableRationalMatrix2D: The REF form of the given matrix.
    """
    res = matrix.mutable()
    k = 0
    while k < min(res.dimensions):
        res = pivot_matrix(res, k)
        if res[k][k] != 0:
            res = scale_matrix(res, k)
            k += 1
        else:
            res = res.remove_row(k).mutable()
    return res


@provide_reference_impl
def back_substitute(matrix: MutableRationalMatrix2D) -> MutableRationalVector:
    """
    Performs back substitution to solve the system of equations.

    Parameters:
        matrix (MutableRationalMatrix2D): Matrix, in REF form, to solve using back substitution.

    Returns:
        MutableRationalVector: A vector solution to the system of equations that the given
        matrix represents.
    """
    rows = matrix.dimensions[0]
    cols = matrix.dimensions[1]
    for r in range(rows - 1, -1, -1):
        for s in range(r - 1, -1, -1):
            matrix[s][cols - 1] -= (matrix[s][r] * matrix[r][cols - 1])
    res = MutableRationalVector(dimensions=rows)
    for i in range(rows):
        res[i] = matrix[i][cols - 1]
    return res


@provide_reference_impl
def gaussian_elimination(A: MutableRationalMatrix2D, b: MutableRationalMatrix2D) -> MutableRationalVector:
    """
    Performs gaussian elimination on the system of equations defined by A and b.

    Parameters:
        A (MutableRationalMatrix2D): Matrix that represents the coefficients of the system of equations.
        b (MutableRationalMatrix2D): Matrix that represents the answers to the system of equations.

    Returns:
        MutableRationalVector: A vector that represents the solution to the system of equations that A and b represent.
    """
    a = (A | b).mutable()
    e = ref(a)

    return back_substitute(e)
