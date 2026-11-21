from support.chem_types import Gram, Mol
from support.chem_types import Solution, CompoundString

from src.elements import molar_mass, grams_to_mols
from src.limiting import limiting_reactant
from driver import provide_reference_impl


def mols_to_grams(comp: CompoundString, mols: Mol) -> Gram:
    """
    Converts moles of a compound to grams based on its molar mass.

    Args:
        comp (CompoundString): compound of interest.
        mols (Mol): amount of the compound in moles.

    Returns:
        Gram: equivalent mass of the compound in grams.
    """
    return mols * molar_mass(comp)


# See elements.py if you have questions about this line.
@provide_reference_impl
def theoretical_yield(solution: Solution, G: dict[CompoundString, Gram], grams: bool = False) -> dict[CompoundString, Gram] | dict[CompoundString, Mol]:
    """
    Calculates the theoretical yield of products in a reaction based on the 
    limiting reactant.

    Args:
        solution (Solution): dictionary with compounds as keys and their 
        required mole ratios as values.
        G (dict[CompoundString, Gram]): dictionary of compounds with their 
        masses in grams.
        grams (bool, optional): if True, returns the yield in grams; 
        if False, in moles. Defaults to False.

    Returns:
        dict[CompoundString, Gram] | dict[CompoundString, Mol]: dictionary of 
        compounds with their theoretical yields, either in grams or moles, 
        depending on the `grams` argument.
    """
    limiting = limiting_reactant(solution, G)
    mole_ratio = grams_to_mols(limiting, G[limiting]) / solution[limiting]
    res = {}

    for comp in solution:
        if comp not in G:
            yield_mols = mole_ratio * solution[comp]
            if grams:
                res[comp] = mols_to_grams(comp, yield_mols)
            else:
                res[comp] = yield_mols
    return res
