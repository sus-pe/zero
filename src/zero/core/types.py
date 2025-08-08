from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction

type PositiveInt = int
type AspectRatio = Fraction


@dataclass(frozen=True)
class Pixels:
    value: PositiveInt

    def __post_init__(self) -> None:
        if self.value <= 0:
            msg = "Pixels must be positive"
            raise ValueError(msg)

    def __int__(self) -> int:
        return self.value

    def __truediv__(self, other: "Pixels") -> float:
        return int(self) / int(other)


@dataclass(frozen=True)
class Resolution:
    width: Pixels
    height: Pixels
    aspect_ratio: AspectRatio = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "aspect_ratio",
            Fraction(self.width.value, self.height.value),
        )

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return int(self.width)
        if index == 1:
            return int(self.height)
        msg = "Resolution only has two dimensions"
        raise IndexError(msg)

    def __len__(self) -> int:
        return 2


class DisplayResolution(Enum):
    SD_4_3 = Resolution(Pixels(640), Pixels(480))
    HD_720P = Resolution(Pixels(1280), Pixels(720))
    FHD_1080P = Resolution(Pixels(1920), Pixels(1080))
    QHD_1440P = Resolution(Pixels(2560), Pixels(1440))
    UWQHD_21_9 = Resolution(Pixels(3440), Pixels(1440))
    UHD_4K = Resolution(Pixels(3840), Pixels(2160))

    @property
    def width(self) -> Pixels:
        return self.value.width

    @property
    def height(self) -> Pixels:
        return self.value.height

    @property
    def aspect_ratio(self) -> AspectRatio:
        return self.value.aspect_ratio

    def __iter__(self) -> Iterator[Pixels]:
        yield self.value.width
        yield self.value.height

    def __repr__(self) -> str:
        return f"{self.name} {self.width}x{self.height}"
