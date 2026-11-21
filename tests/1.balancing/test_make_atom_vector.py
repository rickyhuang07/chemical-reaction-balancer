import pytest
from support.chem_types import CompoundString, CompoundDict, Element
from support.matrix import RationalVector
from support.parser import parse_compound
from tests.helpers.atom_vector_test_data import ATOM_VECTOR_TEST_DATA
from tests.helpers.naming import apply_names

from src.solver import make_atom_vector


@pytest.mark.parametrize('atoms, ucompound, c', apply_names('make_atom_vector', [True, False, True], ATOM_VECTOR_TEST_DATA, noparens=""))
def test_make_atom_vector(atoms: list[Element], c: CompoundString, ucompound: CompoundString):
    pc: CompoundDict = parse_compound(c)
    vec: RationalVector = make_atom_vector(atoms, pc)
    assert len(vec) == len(atoms)
    for i, atom in enumerate(atoms):
        assert (pc[atom] if atom in pc else 0) == vec[i], f"The expected output was {pc[atom] if atom in pc else 0}, but your output was {vec[i]}."
