__all__ = ["convert", "is_compatible", "is_equivalent"]

from math import isclose

from .ast import Dynamic, Unit
from .to_pint import to_pint


def is_equivalent(first: Unit, second: Unit) -> bool:
    if isinstance(first, Dynamic) or isinstance(second, Dynamic):
        return True

    # Yes, this is how this is done: https://stackoverflow.com/a/69637655/1485877
    ratio = ((1 * to_pint(first)) / (1 * to_pint(second))).to_base_units()
    return ratio.dimensionless and isclose(ratio.magnitude, 1)


def is_compatible(first: Unit, second: Unit) -> bool:
    if isinstance(first, Dynamic) or isinstance(second, Dynamic):
        return True

    return to_pint(first).is_compatible_with(to_pint(second))


def convert(first: Unit, second: Unit) -> float:
    if isinstance(first, Dynamic) or isinstance(second, Dynamic):
        return 1

    try:
        return (1 * to_pint(first)).to(to_pint(second)).magnitude
    except Exception:
        raise ValueError(f"Cannot convert {first} to {second}, incompatible units.") from None
