from dataclasses import dataclass

from pydantic import NonNegativeInt, BaseModel


class NonNegativeType(BaseModel):
    value: NonNegativeInt


class Loops(NonNegativeType):
    pass


class Pixels(NonNegativeType):
    pass


@dataclass(frozen=True)
class Resolution:
    width: Pixels
    height: Pixels
