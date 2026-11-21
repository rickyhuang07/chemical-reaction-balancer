import pytest
from support.chem_types import CompoundString, Gram, Solution
from tests.helpers.naming import apply_names
from tests.helpers.chem_helpers import generate
from driver import driver_import_reference

from src.chemical_yield import theoretical_yield
ref_theo = driver_import_reference('chemical_yield.theoretical_yield')


@pytest.mark.parametrize('solution, G', apply_names('theoretical_yield', [True, True], [generate(seed) for seed in range(50)], noparens=""))
def test_theoretical_yield(solution: Solution, G: dict[CompoundString, Gram]):
    for grams in [True, False]:
        correct: dict = ref_theo(solution, dict(G), grams)
        out: dict = theoretical_yield(solution, dict(G), grams)
        assert correct.keys() == out.keys(), ("All elements with non-zero yield should be present in the dictionary. "
                                              "No elements with zero yield should be present in the dictionary.")
        for elem in correct.keys():
            assert round(correct[elem], ndigits=4) == round(out[elem], ndigits=4), f"Yield incorrect for element {elem}."
