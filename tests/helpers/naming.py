from typing import Any, Type
from _pytest.mark.structures import ParameterSet
import pytest


def trans(x: Any) -> str:
    return str(x)


def apply_names(func: str, args: list[str | bool], tests: list[Any], noparens: bool | str = False) -> list[ParameterSet]:
    cases: list[ParameterSet] = []
    for case in tests:
        extra: str = ", ".join(str(args[i]) + trans(x) for i, x in enumerate(case)
                               if (args[i] is not True and args[i] is not False))
        cases.append(
            pytest.param(
                *case, id=func + ("(" if not noparens else "") + ", ".join(trans(x) for i, x in enumerate(
                    case) if args[i] is True) + (")" if not noparens else str(noparens)) + ((", " + extra) if extra else "")
            )
        )
    return cases
