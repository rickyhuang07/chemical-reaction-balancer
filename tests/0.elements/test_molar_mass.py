import pytest
from support.chem_types import CompoundString
from tests.helpers.naming import apply_names
from tests.helpers.chem_helpers import generate_compounds

from src.elements import molar_mass
from driver import driver_import_reference

ref_elem_molar_mass = driver_import_reference('elements.molar_mass')


@pytest.mark.parametrize('unp_comp', apply_names('molar_mass', [True], [generate_compounds(seed, 1) for seed in range(50)], noparens=""))
def test_molar_mass(unp_comp: CompoundString):
    assert round(ref_elem_molar_mass(unp_comp), ndigits=3) == round(molar_mass(unp_comp), ndigits=3), (
        f"The expected output was {ref_elem_molar_mass(unp_comp)}, but your output was {molar_mass(unp_comp)}.")
