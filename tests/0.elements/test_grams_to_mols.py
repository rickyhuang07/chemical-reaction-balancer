import pytest
from support.chem_types import CompoundString, Gram
from tests.helpers.naming import apply_names
from tests.helpers.chem_helpers import generate_compounds, generate_grams
from driver import driver_import_reference

from src.elements import grams_to_mols

ref_grams2mol = driver_import_reference('elements.grams_to_mols')


@pytest.mark.parametrize('comp, g', apply_names('grams_to_mols', [True, False], [(generate_compounds(seed, 1)[0], generate_grams(seed, 1)[0]) for seed in range(50)], noparens=""))
def test_grams_to_mols(comp: CompoundString, g: Gram):
    out = grams_to_mols(comp, g)
    correct = ref_grams2mol(comp, g)
    assert round(correct, ndigits=6) == round(out, ndigits=6)
