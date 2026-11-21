import random
from fractions import Fraction
from support.matrix import MutableRationalMatrix2D, RationalMatrix2D


def generate_random_matrix(seed: int, n: int | None = None, m: int | None = None) -> RationalMatrix2D:
    random.seed(seed)
    if n is None:
        n = random.randint(1, 20)
    if m is None:
        m = random.randint(1, 20)
    matrix: RationalMatrix2D = MutableRationalMatrix2D((n, m))
    for i in range(n):
        for j in range(m):
            matrix[i][j] = Fraction(random.randint(-1000, 1000))
    return matrix

from tests.helpers.matrix_ref_data import REFABLE_MATRICES 
from tests.helpers.pivot_ref_data import PIVOT_MATRICES


def _choose_random_matrices(source, k: int, seed: int | None) -> list[list[RationalMatrix2D]]:
    if seed is not None:
        random.seed(seed)
    if k == 0:
        k = len(source)
    mats = []
    for x in random.choices(source, k=k):
        mat = RationalMatrix2D((len(x), len(x[0])))
        for i in range(mat.dimensions[0]):
            for j in range(mat.dimensions[1]):
                mat[i][j] = Fraction(x[i][j])
        mats.append([mat])
    return mats


def generate_random_refable_matrices(k: int = 0, seed: int | None = None) -> list[list[RationalMatrix2D]]:
    return _choose_random_matrices(REFABLE_MATRICES, k, seed)


def generate_random_pivot_matrices(k: int = 0, seed: int | None = None) -> list[list[RationalMatrix2D]]:
    return _choose_random_matrices(PIVOT_MATRICES, k, seed)


def refable_matrix_to_eq(mat: MutableRationalMatrix2D):
    A = RationalMatrix2D((mat.dimensions[0], mat.dimensions[1] - 1))
    b = RationalMatrix2D((mat.dimensions[0], 1))

    for i in range(mat.dimensions[0]):
        for j in range(mat.dimensions[1] - 1):
            A[i][j] = mat[i][j]
        b[i][0] = mat[i][mat.dimensions[1] - 1]

    assert A.dimensions[0] == b.dimensions[0]
    return A, b

