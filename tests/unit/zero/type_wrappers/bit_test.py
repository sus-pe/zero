from zero.type_wrappers.arithmetic import Bit


def test_alternating_bit() -> None:
    for i, b in enumerate(Bit.alternating(100)):
        assert b == i % 2
