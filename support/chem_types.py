from io import TextIOWrapper
import re
from typing import TypedDict

Mol = float
Gram = float
MolarMass = float

f: TextIOWrapper = open('assets/periodic_table.csv', 'r')
lines: list[str] = f.readlines()

header: list[str] = lines[0].split(",")[:-1]
rows: list[list[str]] = [r.split(",")[:-1] for r in lines[1:]]

f.close()

symbol_idx: int = header.index('Symbol')
_ELEMENTS = set([x[symbol_idx] for x in rows])


class Element(str):
    def __new__(cls, s: str):
        if s not in _ELEMENTS:
            raise ValueError(s + " is not a valid element")
        return super().__new__(cls, s)


class PeriodicTableEntry(TypedDict):
    AtomicNumber: int
    Element: str
    MolarMass: MolarMass


PERIODIC_TABLE: dict[Element, PeriodicTableEntry] = {}

atomic_number_id: int = header.index('AtomicNumber')
element_idx: int = header.index('Element')
mass_idx: int = header.index('AtomicMass')

for row in rows:
    element: Element = Element(row[symbol_idx])
    PERIODIC_TABLE[element] = {
        'AtomicNumber': int(row[atomic_number_id]),
        'Element': row[element_idx],
        'MolarMass': MolarMass(float(row[mass_idx]))
    }


CompoundDict = dict[Element, int]
Side = list[CompoundDict]
Equation = tuple[Side, Side]

SUBSCRIPTS = "\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089"


class CompoundString(str):
    def __new__(cls, s: str):
        if not re.match(r"([(]*[A-Z][a-z]*[" + SUBSCRIPTS + "[)]*]*)+", s):
            raise ValueError(s + " is not a valid compound")
        return super().__new__(cls, s)


SideList = list[CompoundString]
UnparsedEquation = tuple[SideList, SideList]

Solution = dict[CompoundString, int]
