from support.chem_types import CompoundString, Gram, Mol, Solution

from driver import provide_reference_impl
from src.elements import grams_to_mols


# See elements.py if you have questions about this line.
@provide_reference_impl
def ratio(comp: CompoundString, solution: Solution, G: dict[CompoundString, Gram]) -> float:
    """
    Calculates the mole ratio of a compound based on its available mass and 
    required moles in the solution.

    Args:
        comp (CompoundString): compound for which the ratio is calculated.
        solution (Solution): dictionary where keys are compounds and values 
        are their required mole ratios in the reaction.
        G (dict[CompoundString, Gram]): dictionary of compounds with their 
        masses in grams.

    Returns:
        float: mole ratio of the compound, representing the amount of 
        substance relative to the reaction requirements.
    """
    mols = grams_to_mols(comp, G[comp])
    return mols / solution[comp]


INF = 'inf'


@provide_reference_impl
def limiting_reactant(solution: Solution, G: dict[CompoundString, Gram]) -> CompoundString:
    """
    Determines the limiting reactant in a chemical reaction.

    Args:
        solution (Solution): dictionary where keys are compounds and values
        are their mole ratios.
        G (dict[CompoundString, Gram]): dictionary of the compounds with their 
        masses in grams.

    Returns:
        CompoundString: compound that is the limiting reactant.
    """
    res = None
    minr = float(INF)
    for comp in G:
        cur = ratio(comp, solution, G)
        if cur < minr:
            minr = cur
            res = comp
    return res
