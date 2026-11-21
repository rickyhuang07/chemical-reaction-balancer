import random
from fractions import Fraction
from support.chem_types import CompoundString, Gram, Solution, Side, Element, SideList
from support.matrix import RationalVector, MutableRationalVector
from support.parser import parse_equation
from tests.helpers.equations import ATOMS_BY_COMPOUND, CHEMICAL_EQUATIONS
from driver import driver_import_reference

balance_equation = driver_import_reference('solver.balance_equation')
ref_get_all_atoms = driver_import_reference('elements.get_all_atoms')


def generate_compounds(seed: int, k: int | None = None) -> list[CompoundString]:
    random.seed(seed)
    compounds: list[CompoundString] = sorted(ATOMS_BY_COMPOUND.keys())
    if k is None:
        k = random.randint(0, len(compounds))
    return random.choices(compounds, k=k)


def generate_grams(seed: int, k: int | None = None) -> list[Gram]:
    random.seed(seed)
    grams: list[Gram] = [random.uniform(0.1, 20) for x in range(50)]
    if k is None:
        k = random.randint(0, len(grams))
    return random.choices(grams, k=k)


def generate_solution(seed: int) -> Solution:
    random.seed(seed)
    eqn = random.choice(CHEMICAL_EQUATIONS)
    solution: Solution = balance_equation(eqn)
    return eqn, solution


def generate(seed: int) -> tuple[dict[CompoundString, int], list[tuple[CompoundString, float]]]:
    eqn, sol = generate_solution(seed)
    react, _ = parse_equation(eqn, False)
    comp = list(react)
    gr = generate_grams(seed, len(comp))
    G = list(zip(comp, gr))
    return (sol, G)


def generate_random_vector(n: int, seed: int) -> RationalVector:
    random.seed(seed)
    vec: RationalVector = MutableRationalVector(dimensions=n)
    for i in range(n):
        vec[i] = Fraction(random.randint(-1000, 1000))
    return vec


def generate_react_prod_atoms(seed: int) -> tuple[Side, Side, list[Element]]:
    random.seed(seed)
    eqn = random.choice(CHEMICAL_EQUATIONS)
    reacts, prods = parse_equation(eqn, True)
    atoms = ref_get_all_atoms(reacts)
    return (reacts, prods, atoms)


def generate_side_atoms(seed: int) -> tuple[Side, list[Element]]:
    random.seed(seed)
    eqn = random.choice(CHEMICAL_EQUATIONS)
    reacts, prods = parse_equation(eqn, True)
    side = random.choice([reacts, prods])
    atoms = ref_get_all_atoms(side)
    return (side, atoms)


def generate_solution_eqn(seed: int) -> tuple[RationalVector, str]:
    random.seed(seed)
    eq = random.choice(CHEMICAL_EQUATIONS)
    reacts, prods = parse_equation(eq, False)
    vec_length = len(reacts) + len(prods)
    solution = generate_random_vector(vec_length, seed)
    return solution, eq
