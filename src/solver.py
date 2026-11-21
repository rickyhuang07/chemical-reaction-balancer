from fractions import Fraction
from math import lcm

from driver import provide_reference_impl

from support.chem_types import Element, CompoundDict, Side, Solution

from support.matrix import MutableRationalMatrix2D, MutableRationalVector, MutableRationalVector
from support.parser import compound_to_str, parse_equation

from src.elements import get_all_atoms
from src.matrix_operations import transpose_matrix, negate_matrix, gaussian_elimination


ERROR_MESSAGE = "Dummy vector must have dimension at least 2."


# See elements.py if you have questions about this line.
@provide_reference_impl
def make_atom_vector(atoms: list[Element], compound: CompoundDict) -> MutableRationalVector:
    """
    Creates a vector where each element is the number of atoms
    for a compound, with the coefficients indexed based on a list of atoms.

    Parameters:
        atoms (list[Element]): List of elements to include in the vector.
        compound (CompoundDict): Mapping of elements to their counts (subscript)
        in the compound.

    Returns:
        MutableRationalVector: A vector with counts of each element from 'atoms'
        in the compound.
    """
    res = MutableRationalVector(dimensions=len(atoms))
    for i in range(len(atoms)):
        res[i] = Fraction(compound.get(atoms[i], 0))
    return res


@provide_reference_impl
def make_compound_matrix(side: Side, atoms: list[Element]) -> MutableRationalMatrix2D:
    """
    Constructs a matrix of atom counts for a list of compounds.

    Parameters:
        side (Side): List of compounds represented as dictionaries mapping
        elements to counts.
        atoms (list[Element]): List of elements to include in the matrix columns.

    Returns:
        MutableRationalMatrix2D: Matrix where each row corresponds to a compound and
        each column corresponds to an element, with entries being the counts of
        each element in each compound.
    """
    res = MutableRationalMatrix2D(dimensions=(len(side), len(atoms)))
    for i in range(len(side)):
        res[i] = make_atom_vector(atoms, side[i])
    return res


@provide_reference_impl
def make_dummy_equation(k: int) -> MutableRationalVector:
    """
    Creates a dummy vector of dimension k, with a 1 in the last position so
    that the last coefficient is fixed. This prevents trivial solutions.

    Parameters:
        k (int): The dimension of the vector. Must be at least 2.

    Returns:
        MutableRationalVector: A vector of dimension `k` with the last element
        set to 1.

    Raises:
        ValueError: If `k` is less than 2.
    """
    if k < 2:
        raise ValueError(ERROR_MESSAGE)
    res = MutableRationalVector(dimensions=k)
    res[k - 1] = Fraction(1)
    return res


@provide_reference_impl
def make_system_of_equations(react: Side, prod: Side, atoms: list[Element]) -> MutableRationalMatrix2D:
    """
    Constructs a matrix representing the system of equations for balancing a
    chemical equation.

    Parameters:
        react (Side): Reactant side of equation.
        prod (Side): Product side of equation, structured like 'react'.
        atoms (list[Element]): List of all elements involved in the reaction.

    Returns:
        MutableRationalMatrix2D: A matrix representing the system of equations, where
        each row corresponds to an element's balance across reactants and products.
        The balance for reactants is positive, and is negative for products.
    """
    r = transpose_matrix(make_compound_matrix(react, atoms))
    p = negate_matrix(transpose_matrix(make_compound_matrix(prod, atoms)))
    res = (r | p).mutable()
    res += make_dummy_equation(res.dimensions[1])
    return res


@provide_reference_impl
def scale_solution(solution: MutableRationalVector) -> MutableRationalVector:
    """
    Scales a rational vector so all entries become integers instead of fractions.

    Parameters:
        solution (RationalVector): A vector of fractions.

    Returns:
        MutableRationalVector: A new vector with integer entries.
    """
    n = 1
    for x in solution:
        n = lcm(n, x.denominator)
    res = MutableRationalVector(dimensions=len(solution))
    for i in range(len(solution)):
        res[i] = solution[i] * n
    return res


@provide_reference_impl
def make_dictionary_solution(solution: MutableRationalVector, eq: str) -> Solution:
    """
    Maps compounds in a chemical equation to their balanced integer coefficients.

    Parameters:
        solution (RationalVector): Vector of coefficients from the balanced equation.
        eq (str): The chemical equation as a string.

    Returns:
        Solution: A dictionary mapping each compound to its integer coefficient.
    """
    temp = parse_equation(eq, False)
    react = temp[0]
    prod = temp[1]
    compounds = react + prod
    res = Solution({})
    for i in range(len(compounds)):
        res[compounds[i]] = int(solution[i])
    return res


@provide_reference_impl
def balance_equation(eq: str) -> Solution:
    """
    Balances a chemical equation and returns the coefficients in a dictionary.

    Parameters:
        eq (str): The unbalanced chemical equation.

    Returns:
        Solution: A dictionary mapping each compound to its integer coefficient.
    """
    temp = parse_equation(eq, True)
    react = temp[0]
    prod = temp[1]
    atoms = get_all_atoms(react)
    a = make_system_of_equations(react, prod, atoms)
    b = MutableRationalMatrix2D(dimensions=(a.dimensions[0], 1))
    b[a.dimensions[0] - 1][0] = Fraction(1)
    solution = scale_solution(gaussian_elimination(a, b))
    return make_dictionary_solution(solution, eq)
