from .. import timing
from decimal import Decimal


def test_resolve_time():
    assert timing.resolve_time(3.11) == 3.1


def test_resolve_times():
    assert timing.resolve_times([3.11, 3.21]) == [3.1, 3.2]


def test_settings():
    settings = timing.Settings()
    assert settings.max_evap_duration == 2000


def test_decimal_times_are_unique():
    times = [1.1, 1.2]
    assert timing.decimal_times_are_unique(times)


def test_decimal_times_are_not_unique():
    times = [1.1, 1.15]
    assert not timing.decimal_times_are_unique(times)


def test_decimal_to_float():
    assert timing.decimal_to_float(Decimal("1.1")) == 1.1


def test_decimals_to_floats():
    assert timing.decimals_to_floats([Decimal("1.25"), Decimal("1.3")]) == [1.2, 1.3]


def test_float_to_decimal():
    assert timing.float_to_decimal(76.54) == Decimal("76.5")


def test_floats_to_decimals():
    assert timing.floats_to_decimals([76.54, 23.56]) == [
        Decimal("76.5"),
        Decimal("23.5"),
    ]
