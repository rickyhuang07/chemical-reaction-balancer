from math import lcm
from tests.helpers.chem_helpers import generate_random_vector

from support.chem_types import *
from support.matrix import RationalVector

from src.solver import scale_solution

from tests.helpers.naming import apply_names

import pytest


@pytest.mark.parametrize('solution', apply_names('scale_solution', [True], [[generate_random_vector(10, seed)] for seed in range(10, 50)]))
def test_scale_solution(solution: RationalVector):
    copy = solution.mutable()
    scaled = scale_solution(solution)
    factor = copy[0] / scaled[0]
    correct_factor = lcm(*[x.denominator for x in scaled])
    assert correct_factor == factor, f"The expected factor was {correct_factor}, but your factor was {factor}."
    correct = (1/factor) * copy
    assert correct == scaled, f"Your output does not match the expected output---maybe you forgot to scale it?"
