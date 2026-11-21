
from support.parser import parse_equation
from src.elements import get_all_atoms
from support.chem_types import CompoundDict, Element, Side, SideList, Solution


def check_is_balanced(eqn: str, solution: Solution):
    r, p = parse_equation(eqn, True)
    ur, up = parse_equation(eqn, False)

    def count(atom: Element, side: Side, uside: SideList, sol: Solution):
        count: int = 0
        for i in range(len(side)):
            compound: CompoundDict = side[i]
            count += sol.get(uside[i], 0) * compound.get(atom, 0)
        assert count != 0
        return count

    for atom in get_all_atoms(r):
        assert count(atom, r, ur, solution) == count(
            atom, p, up, solution), atom + " counts don't match up: " + str(count(atom, r, ur, solution)) + " vs. " + str(count(
                atom, p, up, solution))
