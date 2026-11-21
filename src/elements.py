from support.chem_types import PERIODIC_TABLE, MolarMass, Element, CompoundString, CompoundDict, Side, Gram, Mol
from support.parser import parse_compound
from driver import provide_reference_impl


# This '@provide_reference_impl' is called a decorator.
# You don't need to understand what it does, but it's here so that if you choose
# not to implement this function, we will provide the reference implementation
# so all the tests will still work on the functions you do implement.
#
# Remember to add any functions you *do* implement to MY_FUNCTIONS in config.py
# (by uncommenting the relevant line).
# If you decide later you want to use the reference solution, recomment the relevant line.
@provide_reference_impl
def get_all_atoms(compounds: Side) -> list[Element]:
    """
    Extracts and returns a sorted list of unique atoms (elements) present in 
    the given compounds.

    Args:
        compounds (Side): list of compounds, where each compound is iterable
        over its constituent atoms.

    Returns:
        list[Element]: sorted list of unique elements present in the input 
        compounds.
    """
    res = []
    for compound in compounds:
        for element in compound:
            if element not in res:
                res.append(element)
    res = sorted(res)
    return res


MOLARMASS = "MolarMass"


@provide_reference_impl
def molar_mass(unp_comp: CompoundString) -> MolarMass:
    """
    Calculates the molar mass of a given compound string.

    Args:
        unp_comp (CompoundString): string representation of a compound.

    Returns:
        MolarMass: The total molar mass of the compound as a float.
    """
    compound = parse_compound(unp_comp)
    res = 0.0
    for element, count in compound.items():
        res += PERIODIC_TABLE[element][MOLARMASS] * count
    return res


@provide_reference_impl
def grams_to_mols(comp: CompoundString, g: Gram) -> Mol:
    """
    Converts the mass of a compound in grams to moles.

    Args:
        comp (CompoundString): compound of interest.
        g (Gram): mass of the compound in grams.

    Returns:
        Mol: amount of the compound in moles.
    """
    return g / molar_mass(comp)
