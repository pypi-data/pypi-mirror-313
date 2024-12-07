from dataclasses import dataclass

from abm._sdk.expression import Unit


@dataclass(frozen=True)
class Parameter:
    value: float
    unit: Unit | None = None
