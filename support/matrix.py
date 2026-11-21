
from copy import deepcopy
from fractions import Fraction
from typing import Iterator, Sequence, overload


class RationalVector():
    dimensions: int
    _data: list[Fraction]

    def __init__(self, *vals, dimensions: int = -1) -> None:
        if len(vals) == 0 and dimensions == -1:
            raise ValueError("Must provide either a set of values or initial dimensions.")
        if dimensions != -1:
            if len(vals) != 0 and len(vals) != dimensions:
                raise ValueError("The values must match the dimensions")
            self.dimensions: int = dimensions
        else:
            self.dimensions = len(vals)
        self._data = [Fraction(0) for _ in range(self.dimensions)]
        for i, x in enumerate(vals):
            self._data[i] = Fraction(x)

    def __getitem__(self, key: int) -> Fraction:
        if 0 > key or key >= self.dimensions:
            raise IndexError("That's an invalid dimension!")
        return self._data[key]

    def mutable(self) -> 'MutableRationalVector':
        row = MutableRationalVector(dimensions=self.dimensions)
        row._data = deepcopy(self._data)
        return row

    @overload
    def __mul__(self, other: Fraction) -> 'RationalVector': ...

    @overload
    def __mul__(self, other: 'RationalVector') -> Fraction: ...

    def __mul__(self, other):
        if isinstance(other, Fraction):
            row: MutableRationalVector = self.mutable()
            row._data = [other * x for x in self._data]
            return row
        elif isinstance(other, RationalVector):
            if self.dimensions != other.dimensions:
                raise TypeError(
                    "Dimensions of vectors in a dot product must be the same")
            return sum([x * y for x, y in zip(self, other)])
        else:
            raise TypeError()

    __rmul__ = __mul__

    def is_zero_vector(self):
        return set(self._data) == set([Fraction(0)])

    def __add__(self, other: 'MutableRationalVector | Fraction') -> 'MutableRationalVector':
        if isinstance(other, RationalVector):
            mat: RationalVector
            assert self.dimensions == other.dimensions, "Dimensions of rows to add together must match."
            mat = MutableRationalVector(dimensions=self.dimensions)
            mat._data = [x + y for x, y in zip(self._data, other._data)]
            return mat
        else:
            mat = MutableRationalVector(
                dimensions=self.dimensions + 1)
            mat[-1] = other
            return mat

    def __sub__(self, other: 'RationalVector') -> 'RationalVector':
        assert self.dimensions == other.dimensions, "Dimensions of rows to subtract must match."
        mat: RationalVector = MutableRationalVector(dimensions=self.dimensions)
        mat._data = [x - y for x, y in zip(self._data, other._data)]
        return mat

    def __or__(self, other: 'MutableRationalVector') -> 'MutableRationalVector':
        row: MutableRationalVector = self.mutable()
        row._data += other._data
        row.dimensions = len(self._data) + len(other._data)
        return row

    def __repr__(self):
        return ", ".join([str(x.numerator) if x.denominator == 1 else str(x.numerator) + "/" + str(x.denominator) for x in self._data])

    def __str__(self):
        return str(self._data)

    def __len__(self):
        return self.dimensions

    def __iter__(self) -> Iterator[Fraction]:
        return iter(self._data)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MutableRationalVector):
            return self._data == other._data
        return False


class MutableRationalVector(RationalVector):
    @property
    def data(self) -> list[Fraction]:
        return list(deepcopy(self._data))

    def __setitem__(self, key: int, value: Fraction) -> None:
        if 0 > key or key >= self.dimensions:
            raise IndexError("That's an invalid dimension!")
        self._data[key] = value

    def immutable(self) -> RationalVector:
        return self


class RationalMatrix2D():
    _data: list[MutableRationalVector]

    def __init__(self, dimensions: tuple[int, int]) -> None:
        self.dimensions: tuple[int, int] = dimensions
        self._data: list[MutableRationalVector] = [
            MutableRationalVector(dimensions=dimensions[1]) for _ in range(dimensions[0])
        ]

    def mutable(self):
        mat = MutableRationalMatrix2D(self.dimensions)
        mat._data = [row.mutable() for row in self._data]
        return mat

    @property
    def rows(self) -> Sequence[RationalVector]:
        return tuple([x for x in self._data])

    def swap_rows(self, i: int, j: int) -> 'MutableRationalMatrix2D':
        mat: MutableRationalMatrix2D = self.mutable()
        mat._data[i] = self._data[j]
        mat._data[j] = self._data[i]
        return mat

    def remove_row(self, i: int) -> 'MutableRationalMatrix2D':
        mat: MutableRationalMatrix2D = self.mutable()
        mat._data.pop(i)
        mat.dimensions = (mat.dimensions[0] - 1, mat.dimensions[1])
        return mat

    def __getitem__(self, key: int) -> MutableRationalVector:
        if 0 > key or key >= self.dimensions[0]:
            raise IndexError("That's an invalid dimension!")
        return self._data[key]

    def __add__(self, other: 'RationalVector | RationalMatrix2D') -> 'RationalMatrix2D':
        r: int = self.dimensions[0]
        c: int = self.dimensions[1]

        mat: MutableRationalMatrix2D = self.mutable()
        if isinstance(other, RationalVector):
            assert self.dimensions[1] == other.dimensions, "Dimensions of rows in a matrix must match."
            r += 1
            mat._data.append(other.mutable())
        else:
            assert self.dimensions == other.dimensions, "Dimensions of rows to add together must match."
            mat = self.mutable()
            for i in range(r):
                for j in range(c):
                    mat[i][j] += other[i][j]

        mat.dimensions = (r, c)
        return mat

    def __or__(self, other: 'RationalMatrix2D') -> 'RationalMatrix2D':
        assert (self.dimensions[0] == other.dimensions[0])
        mat: MutableRationalMatrix2D = MutableRationalMatrix2D(
            (self.dimensions[0], self.dimensions[1] + other.dimensions[1]))
        for i in range(other.dimensions[0]):
            mat[i] = self[i] | other[i]
        return mat

    def __repr__(self):
        return '[' + ', '.join(('[' + repr(row) + "]" for row in self._data)) + ']'

    def __str__(self):
        return '[\n ' + ' '.join((' [' + repr(row) + "]\n" for row in self._data)) + ']'

    def __len__(self):
        return self.dimensions[0]

    def __iter__(self) -> Iterator[MutableRationalVector]:
        return iter(self._data)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RationalMatrix2D):
            return self._data == other._data
        return False


class MutableRationalMatrix2D(RationalMatrix2D):
    def __setitem__(self, key: int, value: RationalVector) -> None:
        if 0 > key or key >= self.dimensions[0]:
            raise IndexError("That's an invalid dimension!")
        self._data[key] = value.mutable()

