import pytest
from support.chem_types import CompoundString, Gram, Solution
from tests.helpers.naming import apply_names
from tests.helpers.chem_helpers import generate
from driver import driver_import_reference

ref_ratio = driver_import_reference('limiting.ratio')

from src.limiting import ratio


@pytest.mark.parametrize('solution, G', apply_names('ratio', [False, True, False], [generate(seed) for seed in range(50)], noparens=""))
def test_ratio(solution: Solution, G: dict[CompoundString, Gram]):
    for comp, _ in G:
        correct = ref_ratio(comp, solution, dict(G))
        out = ratio(comp, solution, dict(G))
        assert round(correct, ndigits=4) == round(out, ndigits=4)
