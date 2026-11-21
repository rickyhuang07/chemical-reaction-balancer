import pytest
from support.chem_types import CompoundString, Gram
from tests.helpers.naming import apply_names
from tests.helpers.chem_helpers import generate
from driver import driver_import_reference
from fractions import Fraction

ref_limiting = driver_import_reference('limiting.limiting_reactant')

from src.limiting import limiting_reactant


@pytest.mark.parametrize('solution, G', apply_names('limiting_reactant', [True, False], [generate(seed) for seed in range(50)], noparens=""))
def test_limiting_reactant(solution, G: dict[CompoundString, Gram]):
    correct = ref_limiting(solution, dict(G))
    out = limiting_reactant(solution, dict(G))
    assert correct == out
