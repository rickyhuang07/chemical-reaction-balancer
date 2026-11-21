from typing import Iterable, TypeVar
from support.chem_types import CompoundString
from support.chem_types import PERIODIC_TABLE, Element
from support.parser import parse_compound, parse_equation


CHEMICAL_EQUATIONS: list[str] = [
    "F\u2082 + FeI\u2083 \u2192 I\u2082 + FeF\u2083",
    "Sn + H\u2082SO\u2084 \u2192 SnSO\u2084 + H\u2082",
    "Al + NiBr\u2082 \u2192 AlBr\u2083 + Ni",
    "Fe(NO\u2083)\u2083 + Al \u2192 Al(NO\u2083)\u2083 + Fe",
    "NaI + Cl\u2082 \u2192 NaCl + I\u2082",
    "Zn(NO\u2083)\u2082 + NaOH \u2192 Zn(OH)\u2082 + NaNO\u2083",
    "HCl + Na\u2082S \u2192 NaCl + H\u2082S",
    "Pb(NO\u2083)\u2082 + KBr \u2192 PbBr\u2082 + KNO\u2083",
    "K\u2082O + MgCO\u2083 \u2192 K\u2082CO\u2083 + MgO",
    "Pb(NO\u2083)\u2082 + KBr \u2192 PbBr\u2082 + KNO\u2083",
    "K\u2083PO\u2084 + SrCl\u2082 \u2192 Sr\u2083(PO\u2084)\u2082 + KCl",
    "NaOH + MgCl\u2082 \u2192 NaCl + Mg(OH)\u2082",
    "KBr + AgC\u2082H\u2083O\u2082 \u2192 KC\u2082H\u2083O\u2082 + AgBr",
    "MgSO\u2084 + Ba(NO\u2083)\u2082 \u2192 Mg(NO\u2083)\u2082 + BaSO\u2084",
    "Fe\u2082O\u2083 + SO\u2083 \u2192 Fe\u2082(SO\u2084)\u2083",
    "NaCl + AgNO\u2083 \u2192 AgCl + NaNO\u2083",
    "(NH\u2084)\u2082Cr\u2082O\u2087 \u2192 Cr\u2082O\u2083 + H\u2082O + N\u2082",
    "CH\u2084 + O\u2082 \u2192 CO\u2082 + H\u2082O",
    "C\u2081\u2082H\u2082\u2086 + O\u2082 \u2192 CO\u2082 + H\u2082O",
    "C\u2082H\u2085OH + O\u2082 \u2192 CO\u2082 + H\u2082O",
    "C\u2082H\u2082N\u2082O\u2084 + O\u2082 \u2192 CO\u2082 + H\u2082O + N\u2082",
    "NaCl + AgNO\u2083 \u2192 AgCl + NaNO\u2083",
    "CaO + CO\u2082 \u2192 CaCO\u2083",
    "H\u2082 + Cl\u2082 \u2192 HCl",
    "HBr + Cl\u2082 \u2192 HCl + Br\u2082",
    "SO\u2082 + O\u2082 \u2192 SO\u2083",
    "C + H\u2082 \u2192 C\u2086H\u2086",
    "Na + C + O\u2082 \u2192 Na\u2082CO\u2083",
    "Na\u2082CO\u2083 \u2192 Na\u2082O + CO\u2082",
    "HCl + NaOH \u2192 NaCl + H\u2082O",
    "CaCO\u2083 \u2192 CaO + CO\u2082",
    "O\u2082 \u2192 O\u2083",
    "KClO\u2083 \u2192 KCl + O\u2082",
    "Na\u2082O + CO\u2082 \u2192 Na\u2082CO\u2083",
    "H\u2082SO\u2083 \u2192 H\u2082O + SO\u2082",
    "C\u2087H\u2085N\u2083O\u2086 \u2192 N\u2082 + H\u2082O + CO + C",
    "C\u2086H\u2081\u2082O\u2086 + O\u2082 \u2192 CO\u2082 + H\u2082O",
    "Fe\u2082S\u2083 + O\u2082 \u2192 Fe\u2082O\u2083 + SO\u2082",
    "CH\u2084 + F\u2082 \u2192 CF\u2084 + H\u2082",
    "H\u2082 + O\u2082 \u2192 H\u2082O",
    "P\u2084 + O\u2082 \u2192 P\u2082O\u2085",
    "Al\u2082S\u2083 + O\u2082 \u2192 Al\u2082O\u2083 + SO\u2082",
    "C\u2082H\u2084 + O\u2082 \u2192 C\u2082H\u2084O\u2082",
    "C\u2082H\u2084 + Cl\u2082 \u2192 C\u2082H\u2084Cl\u2082",
    "HNO\u2083 + Ba(OH)\u2082 \u2192 H\u2082O + Ba(NO\u2083)\u2082",
    "HNO\u2083 + Ba(OH)\u2082 \u2192 H\u2082O + Ba(NO\u2083)\u2082",
    "H\u2083PO\u2084 + Ca(OH)\u2082 \u2192 H\u2082O + Ca\u2083(PO\u2084)\u2082",
    "K + Br\u2082 \u2192 KBr",
    "NaCl + AgNO\u2083 \u2192 NaNO\u2083 + AgCl",
    "Ca + O\u2082  \u2192 CaO",
    "Fe + S\u2088 \u2192 Fe\u2082S\u2083",
    "Li + O\u2082  \u2192 Li\u2082O\u2082",
    "NO + Cl\u2082 \u2192 NOCl",
    "Fe + SO\u2083 \u2192 FeSO\u2083",
    "KrF\u2082 + H\u2082O \u2192 Kr + HF + O\u2082",
    "SO\u2083 + SCl\u2082 \u2192 SOCl\u2082 + SO\u2082",
    "K + MgCl\u2082 \u2192 KCl + Mg",
    "C\u2087H\u2081\u2086 + O\u2082 \u2192 CO\u2082 + H\u2082O",
    "H\u2082 + O\u2082 \u2192 H\u2082O",
    "C\u2083H\u2088 + O\u2082 \u2192 CO\u2082 + H\u2082O",
    "CO\u2082 + H\u2082O \u2192 C\u2086H\u2081\u2082O\u2086 + O\u2082",
    "SiCl\u2084 + H\u2082O \u2192 H\u2084SiO\u2084 + HCl",
    "Al + HCl \u2192 AlCl\u2083 + H\u2082",
    "Na\u2082CO\u2083 + HCl \u2192 NaCl + H\u2082O + CO\u2082",
    "C\u2087H\u2086O\u2082 + O\u2082 \u2192 CO\u2082 + H\u2082O",
    "KClO\u2083 \u2192 KClO\u2084 + KCl",
    "H\u2082SO\u2084 + HI \u2192 H\u2082S + I\u2082 + H\u2082O",
    "Fe\u2082(SO\u2084)\u2083 + KOH \u2192 K\u2082SO\u2084 + Fe(OH)\u2083",
    "Ca\u2083(PO\u2084)\u2082 + SiO\u2082 \u2192 P\u2084O\u2081\u2080 + CaSiO\u2083",
    "Al\u2082(SO\u2084)\u2083 + Ca(OH)\u2082 \u2192 Al(OH)\u2083 + CaSO\u2084",
]

# for e in CHEMICAL_EQUATIONS:
#    left, right = parse_equation(e, True)
#    if get_all_atoms(left) is None or get_all_atoms(right) is None:
#        assert False
#    #assert set(get_all_atoms(left)) ^ set(get_all_atoms(right)) == set()

T = TypeVar('T')


def flatten(L: Iterable[Iterable[T]]) -> Iterable[T]:
    return [x for y in L for x in y]


COMPOUNDS: set[CompoundString] = set(flatten(flatten([
    parse_equation(eqn, False) for eqn in CHEMICAL_EQUATIONS
])))

USED_ATOMS: set[Element] = set(flatten(
    parse_compound(x) for x in COMPOUNDS
))

ATOMS: set[Element] = set(PERIODIC_TABLE.keys())
ATOMS_BY_COMPOUND: dict[CompoundString, set[Element]] = dict([('H\u2082O', {'H', 'O'}), ('Li', {'Li'}), ('SCl\u2082', {'S', 'Cl'}), ('Al\u2082O\u2083', {'Al', 'O'}), ('Al\u2082S\u2083', {'S', 'Al'}), ('Kr', {'Kr'}), ('O\u2083', {'O'}), ('CaSiO\u2083', {'Ca', 'Si', 'O'}), ('KCl', {'K', 'Cl'}), ('P\u2084', {'P'}), ('K\u2082O', {'K', 'O'}), ('FeF\u2083', {'F', 'Fe'}), ('K\u2082CO\u2083', {'C', 'K', 'O'}), ('SO\u2083', {'S', 'O'}), ('SrCl\u2082', {'Sr', 'Cl'}), ('Zn(NO\u2083)\u2082', {'Zn', 'N', 'O'}), ('C\u2082H\u2082N\u2082O\u2084', {'N', 'C', 'H', 'O'}), ('C\u2086H\u2081\u2082O\u2086', {'C', 'H', 'O'}), ('MgCl\u2082', {'Mg', 'Cl'}), ('K\u2083PO\u2084', {'P', 'K', 'O'}), ('C\u2082H\u2084O\u2082', {'C', 'H', 'O'}), ('S\u2088', {'S'}), ('Ca', {'Ca'}), ('SOCl\u2082', {'S', 'O', 'Cl'}), ('AgNO\u2083', {'N', 'O', 'Ag'}), ('AgC\u2082H\u2083O\u2082', {'C', 'H', 'O', 'Ag'}), ('HF', {'F', 'H'}), ('Al\u2082(SO\u2084)\u2083', {'S', 'Al', 'O'}), ('C\u2082H\u2084', {'C', 'H'}), ('Pb(NO\u2083)\u2082', {'Pb', 'N', 'O'}), ('SiO\u2082', {'Si', 'O'}), ('CaO', {'Ca', 'O'}), ('SO\u2082', {'S', 'O'}), ('Br\u2082', {'Br'}), ('H\u2082', {'H'}), ('H\u2084SiO\u2084', {'H', 'O', 'Si'}), ('Ca\u2083(PO\u2084)\u2082', {'Ca', 'P', 'O'}), ('C\u2086H\u2086', {'C', 'H'}), ('KC\u2082H\u2083O\u2082', {'H', 'C', 'K', 'O'}), ('Mg', {'Mg'}), ('PbBr\u2082', {'Br', 'Pb'}), ('HI', {'I', 'H'}), ('Fe(OH)\u2083', {'O', 'H', 'Fe'}), ('Fe(NO\u2083)\u2083', {'O', 'N', 'Fe'}), ('AgBr', {'Br', 'Ag'}), ('H\u2083PO\u2084', {'P', 'H', 'O'}), ('LiZn', {'Zn', 'Li'}), ('Al(NO\u2083)\u2083', {'Al', 'N', 'O'}), ('NaOH', {'H', 'O', 'Na'}), ('NiBr\u2082', {'Ni', 'Br'}), ('CaCO\u2083', {'Ca', 'C', 'O'}), ('NaCl', {'Cl', 'Na'}), ('(NH\u2084)\u2082Cr\u2082O\u2087', {'H', 'O', 'N', 'Cr'}), ('KBr', {'Br', 'K'}), ('Li\u2082O\u2082', {'Li', 'O'}), ('O\u2082', {'O'}), ('NaNO\u2083', {'N', 'O', 'Na'}), ('Ba(OH)\u2082', {'H', 'O', 'Ba'}), ('KrF\u2082', {'Kr', 'F'}), ('F\u2082', {'F'}), ('Sn', {'Sn'}), (
    'Zn(OH)\u2082', {'Zn', 'H', 'O'}), ('K', {'K'}), ('KClO\u2084', {'K', 'O', 'Cl'}), ('NOCl', {'N', 'O', 'Cl'}), ('Ba(NO\u2083)\u2082', {'N', 'O', 'Ba'}), ('CH\u2084', {'C', 'H'}), ('Fe\u2082(SO\u2084)\u2083', {'S', 'O', 'Fe'}), ('Fe\u2082O\u2083', {'O', 'Fe'}), ('NaI', {'I', 'Na'}), ('Cl\u2082', {'Cl'}), ('SiCl\u2084', {'Si', 'Cl'}), ('Sr\u2083(PO\u2084)\u2082', {'Sr', 'P', 'O'}), ('P\u2084O\u2081\u2080', {'P', 'O'}), ('C\u2082H\u2085OH', {'C', 'H', 'O'}), ('C\u2087H\u2081\u2086', {'C', 'H'}), ('Fe(NO\u2083)\u2082', {'O', 'N', 'Fe'}), ('C\u2082H\u2084Cl\u2082', {'C', 'H', 'Cl'}), ('H\u2082SO\u2083', {'S', 'H', 'O'}), ('FeSO\u2083', {'S', 'O', 'Fe'}), ('AgCl', {'Cl', 'Ag'}), ('C\u2087H\u2086O\u2082', {'C', 'H', 'O'}), ('C\u2081\u2082H\u2082\u2086', {'C', 'H'}), ('HBr', {'Br', 'H'}), ('KOH', {'H', 'K', 'O'}), ('CF\u2084', {'F', 'C'}), ('C', {'C'}), ('MgCO\u2083', {'Mg', 'C', 'O'}), ('CO\u2082', {'C', 'O'}), ('P\u2082O\u2085', {'P', 'O'}), ('Na\u2082S', {'S', 'Na'}), ('C\u2083H\u2088', {'C', 'H'}), ('H\u2082SO\u2084', {'S', 'H', 'O'}), ('KNO\u2083', {'N', 'K', 'O'}), ('HCl', {'H', 'Cl'}), ('Na', {'Na'}), ('Fe', {'Fe'}), ('I\u2082', {'I'}), ('C\u2087H\u2085N\u2083O\u2086', {'N', 'C', 'H', 'O'}), ('AlCl\u2083', {'Al', 'Cl'}), ('MgO', {'Mg', 'O'}), ('KClO\u2083', {'K', 'O', 'Cl'}), ('Cr\u2082O\u2083', {'O', 'Cr'}), ('SnSO\u2084', {'S', 'Sn', 'O'}), ('H\u2082S', {'S', 'H'}), ('N\u2082', {'N'}), ('Mg(NO\u2083)\u2082', {'Mg', 'N', 'O'}), ('CaSO\u2084', {'Ca', 'S', 'O'}), ('Na\u2082CO\u2083', {'C', 'O', 'Na'}), ('Mg(OH)\u2082', {'Mg', 'H', 'O'}), ('AlBr\u2083', {'Br', 'Al'}), ('Al', {'Al'}), ('BaSO\u2084', {'S', 'O', 'Ba'}), ('Ni', {'Ni'}), ('HNO\u2083', {'N', 'H', 'O'}), ('FeI\u2083', {'I', 'Fe'}), ('K\u2082SO\u2084', {'S', 'K', 'O'}), ('Ca(OH)\u2082', {'Ca', 'H', 'O'}), ('CO', {'C', 'O'}), ('Fe\u2082S\u2083', {'S', 'Fe'}), ('MgSO\u2084', {'S', 'Mg', 'O'}), ('Na\u2082O', {'O', 'Na'}), ('NO', {'N', 'O'}), ('Al(OH)\u2083', {'Al', 'H', 'O'})])
