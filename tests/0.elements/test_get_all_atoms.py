import pytest
from support.chem_types import CompoundString, Side, Element
from support.parser import compound_to_str, parse_compound
from tests.helpers.naming import apply_names
from tests.helpers.equations import ATOMS_BY_COMPOUND, flatten
from tests.helpers.chem_helpers import generate_compounds

from src.elements import get_all_atoms


@pytest.mark.parametrize('ucompounds, c', apply_names('get_all_atoms', [False, True], [list(zip(*[[x, compound_to_str(x)] for x in generate_compounds(seed)])) for seed in range(50)], noparens=""))
def test_get_all_atoms(c: list[CompoundString], ucompounds: list[CompoundString]):
    compounds: Side = Side([parse_compound(x) for x in ucompounds])
    atoms: list[Element] = get_all_atoms(compounds)
    assert len(atoms) == len(set(atoms)), "You may have counted some atoms more than once!"
    assert atoms == sorted(atoms), "Your atoms may be out of order. Did you forget to use a function we mentioned in the guide?"
    assert set(
        flatten([ATOMS_BY_COMPOUND[x] for x in ucompounds])) == set(atoms), f"The expected output was {flatten([ATOMS_BY_COMPOUND[x] for x in ucompounds])}, but your output was {set(atoms)}"
