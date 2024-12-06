from dataclasses import dataclass
from decimal import Decimal
from typing import Annotated

import numpy as np
from pydantic import Field, PlainSerializer


@dataclass(frozen=True)
class Settings:
    max_evap_duration: int = 2000  # maximum allowed rf evaporation duration
    max_exp_time: Decimal = Decimal("150.0")  # maximum allowed user experiment time
    min_tof: Decimal = Decimal("2.0")  # minimum allowed value for time-of-flight
    max_tof: Decimal = Decimal("20.0")  # maximum allowed value for time-of-flight


TimeMs = Annotated[
    Decimal,
    Field(ge=Decimal("0.0"), le=Settings.max_exp_time, decimal_places=1),
    PlainSerializer(lambda x: decimal_to_float(x), return_type=float),
]


EndTimeMs = TimeMs


TimeOfFlightMs = Annotated[TimeMs, Field(ge=Settings.min_tof, le=Settings.max_tof)]


def ceiling(x: float, precision=0):
    """Performs ceiling function with caller-specified precision

    Args:
        x (float): _description_
        precision (int, optional): Number of decimal points. Defaults to 0.

    Returns:
        float: output
    """
    return np.true_divide(np.ceil(x * 10**precision), 10**precision)


def floor(x: float, precision=0):
    """Performs ceiling function with caller-specified precision

    Args:
        x (float): _description_
        precision (int, optional): Number of decimal points. Defaults to 0.

    Returns:
        float: output
    """
    return np.true_divide(np.floor(x * 10**precision), 10**precision)


def resolve_time(t: float) -> float:
    """Resolves input time to nearest 0.1 ms, corresponding to the allowed time resolution.

    Args:
        t (float): input time in ms

    Returns:
        float: output time in ms
    """
    return floor(t, 1)


def resolve_times(ts: list) -> list:
    """Resolves input times to nearest 0.1 ms, corresponding to the allowed time resolution.

    Args:
        ts (list): input time in ms

    Returns:
        list: output times in ms
    """
    return [resolve_time(t) for t in ts]


def decimal_times_are_unique(ts: list[Decimal]) -> bool:
    """Tests if all object times are in fact, unique

    Args:
        ts (list): list of times

    Returns:
        bool: true if times are unique
    """
    float_times = decimals_to_floats(ts)
    return all(np.diff(float_times))


def decimal_to_float(d: Decimal) -> float:
    """Converts decimal time to float

    Args:
        d (Decimal): input time in ms
    Returns:
        float: output time in ms, resolved to 0.1 resolution
    """
    return resolve_time(d)


def decimals_to_floats(ds: list[Decimal]) -> list[float]:
    """Converts lists of decimal times to floats

    Args:
        ds (list): input times in ms

    Returns:
        list: output times in ms, resolved to 0.1 resolution
    """
    return resolve_times(ds)


def float_to_decimal(f: float) -> Decimal:
    """Converts float to decimal value with 0.1 resolution

    Args:
        ds (list): input times in ms

    Returns:
        list: output times in ms, resolved to 0.1 resolution
    """
    return Decimal(resolve_time(f))


def floats_to_decimals(fs: list[float]) -> list[Decimal]:
    """Converts lists of decimals to floats

    Args:
        fs (list): input times in ms, as floats

    Returns:
        list: output times in ms, resolved to 0.1 resolution
    """
    return [float_to_decimal(f) for f in fs]
