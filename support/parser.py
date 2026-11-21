from support.chem_types import (
    CompoundDict, CompoundString,
    Element, Equation,
    Side, SideList, SUBSCRIPTS,
    UnparsedEquation,
)
from typing import overload, Literal


def compound_to_str(compound: CompoundString) -> CompoundString:
    for i, x in enumerate(SUBSCRIPTS):
        compound = CompoundString(compound.replace(x, str(i)))
    return compound


def parse_compound(compound: CompoundString) -> CompoundDict:
    output: CompoundDict = CompoundDict({})
    i = 0
    while i < len(compound) and compound[i] != ')':
        atom: str = ""
        atom_inner: CompoundDict | None = None
        if compound[i] == '(':
            start = i + 1
            cnt = 1
            while cnt != 0:
                i += 1
                if compound[i] == '(':
                    cnt += 1
                elif compound[i] == ')':
                    cnt -= 1
            atom_inner = parse_compound(CompoundString(compound[start:i]))
            i += 1
        else:
            assert (compound[i].isupper())
            atom = compound[i]
            i += 1
        while i < len(compound) and compound[i] not in SUBSCRIPTS and not compound[i].isdigit() and not compound[i].isupper() and compound[i] not in ['(', ')']:
            atom = atom + compound[i]
            i += 1
        num: str = ""
        while i < len(compound) and not compound[i].isupper() and compound[i] not in ['(', ')']:
            assert compound[i] in SUBSCRIPTS or compound[i].isnumeric()
            if compound[i] in SUBSCRIPTS:
                num += str(SUBSCRIPTS.index(compound[i]))
            else:
                num += compound[i]
            i += 1
        if atom_inner:
            for x in atom_inner:
                output[x] = (int(num) if num else 1) * atom_inner[x]
        else:
            output[Element(atom)] = int(num) if num else 1
    return output


@overload
def parse_equation(
    eq: str, dictify: Literal[True]) -> Equation: ...


@overload
def parse_equation(
    eq: str, dictify: Literal[False]) -> UnparsedEquation: ...


def parse_equation(eq: str, dictify: bool) -> UnparsedEquation | Equation:
    eq = eq.replace(" ", "")
    if "\u2192" not in eq:
        raise ValueError("All chemical questions must have an '\u2192' in them!")

    split_eq: SideList = SideList(
        [CompoundString(x) for x in eq.split("\u2192")])
    if len(split_eq) != 2:
        raise ValueError(
            "All chemical questions must have exactly two sides in them!")

    left_side: SideList = SideList([
        CompoundString(x) for x in split_eq[0].split("+")])
    right_side: SideList = SideList([
        CompoundString(x) for x in split_eq[1].split("+")])

    if not dictify:
        return (left_side, right_side)

    left = Side([parse_compound(x) for x in left_side])
    right = Side([parse_compound(x) for x in right_side])

    return (left, right)
