from typing import TypedDict

from support.chem_types import CompoundString, Gram, Solution
from support.parser import parse_equation

from src.solver import balance_equation
from src.limiting import limiting_reactant
from src.chemical_yield import theoretical_yield


class Problem(TypedDict):
    eqn: str
    G: dict[CompoundString, Gram]


A: Problem = {
    'eqn': "Fe\u2082O\u2083 + Al \u2192 Fe + Al\u2082O\u2083",
    'G': {CompoundString('Fe\u2082O\u2083'): Gram(20), CompoundString('Al'): Gram(8)}
}

B: Problem = {
    'eqn': "TiCl\u2084 + Mg \u2192 Ti + MgCl\u2082",
    'G': {CompoundString('TiCl\u2084'): Gram(1000), CompoundString('Mg'): Gram(200)}
}

C: Problem = {
    'eqn': "KClO\u2083 \u2192 KCl + O\u2082",
    'G': {CompoundString('KClO\u2083'): Gram(40)}
}

D: Problem = {
    'eqn': "Na\u2082S + AgNO\u2083 \u2192 Ag\u2082S + NaNO\u2083",
    'G': {CompoundString('AgNO\u2083'): Gram(3.94), CompoundString("Na\u2082S"): Gram(10000)}
}

X: Problem = D
solution: Solution = balance_equation(X['eqn'])

react, pprod = parse_equation(X['eqn'], True)

print("The limiting reactant is..." +
      limiting_reactant(solution, X['G']) + "!")
print("The theoretical yield (in mols) is..." +
      str(theoretical_yield(solution, X['G'])))
print("The theoretical yield (in grams) is..." +
      str(theoretical_yield(solution, X['G'], grams=True)))
