# Copyright 2024 Infleqtion
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A module that captures the features, and limitations, of optical objects
implemented by the Oqtant hardware projection system.
"""


from collections.abc import Callable

import numpy as np
from typing import Annotated
from pydantic import Field
from .timing import resolve_time, TimeMs
from decimal import Decimal
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    resolution: float = 2.2  # 1/e^2 diameter of projection system, microns
    position_step: float = 1.0  # grid step between projected spots, microns
    min_position: float = -60.0  # minimum position of projected light, microns
    max_position: float = 60  # maximum position of projected light, microns
    num_projected_spots: int = 121
    update_period: Decimal = Decimal(
        "0.1"
    )  # milliseconds between updates of projected light
    max_energy: float = 100.0  # maximum projected energy shift at any position, kHz
    min_barrier_width: float = 0.5
    max_barrier_width: float = 50
    max_num_barrier_times: int = 20
    max_num_barriers: int = 20
    terminator_position: float = (
        30.0  # position of the center of the gaussian terminator beam in um
    )
    terminator_width: float = 20.7  # 1/e^2 width of the terminator beam in um

    @property
    def projected_spots(self) -> list[float]:
        return np.arange(
            self.min_position,
            self.max_position + self.position_step,
            self.position_step,
        )


settings = Settings()


ProjectedPosition = Annotated[
    float, Field(ge=settings.min_position, le=settings.max_position)
]

ProjectedPositions = Annotated[
    list[ProjectedPosition],
    Field(min_length=2, max_length=settings.num_projected_spots),
]

ProjectedEnergy = Annotated[float, Field(ge=0.0, le=settings.max_energy)]

ProjectedEnergies = Annotated[
    list[ProjectedEnergy], Field(min_length=2, max_length=settings.num_projected_spots)
]

BarrierTime = TimeMs

BarrierTimes = Annotated[
    list[BarrierTime], Field(min_length=2, max_length=settings.max_num_barrier_times)
]

BarrierPosition = ProjectedPosition

BarrierPositions = Annotated[
    ProjectedPositions, Field(max_length=settings.max_num_barriers)
]

BarrierHeight = ProjectedEnergy

BarrierHeights = Annotated[
    ProjectedEnergies, Field(max_length=settings.max_num_barrier_times)
]

BarrierWidth = Annotated[
    float, Field(ge=settings.min_barrier_width, le=settings.max_num_barrier_times)
]

BarrierWidths = Annotated[
    list[BarrierWidth], Field(min_length=2, max_length=settings.max_num_barrier_times)
]

BarrierTimes = Annotated[
    list[TimeMs], Field(min_length=2, max_length=settings.max_num_barrier_times)
]


def get_potential_from_weights(weights: list, positions: list[float]) -> list[float]:
    """Method to calculate projected potential based on given weights (intensities)
    applied to each projected spot

    Args:
        weights: height of each Gaussian spot

    Returns:
        list[float]: Calculated total optical potential at the given positions
    """
    if len(weights) != settings.num_projected_spots:
        raise ValueError(
            f"number of weights values must equal {settings.num_projected_spots}"
        )

    potential = np.zeros_like(positions, dtype=np.float64)
    for indx, spot in enumerate(settings.projected_spots):
        potential += gaussian(
            xs=positions,
            amp=weights[indx],
            center=spot,
            sigma=settings.resolution / 4.0,
            offset=0.0,
        )
    return list(potential)


def get_corrected_projection_weights(
    get_ideal_potential: Callable[[float], list], time: float = 0
) -> np.ndarray:
    """Method to calculate weights for each horizontal "spot" projected onto the atom ensemble to
    attempt to achieve the passed optical object's "ideal" potential energy profile.
    Implements first-order corrections for anamolous contributions from nearby spots,
    inter-integer barrier centers, etc

    Args:
        get_ideal_potential (Callable[[float], list]): Method for the optical object or any class
            that supports optical objects that calculates the specified "ideal" or "requested"
            potential energy profile
        time (float, optional): Time at which to correct

    Returns:
        np.ndarray[float]: Calculated (optical intensity) contribution for each projected spot
            (diffraction frequency) used by the projection systems
    """
    bin_size = 10  # index range of local scaling window
    positions_fine = np.arange(
        settings.min_position - settings.position_step / 2,
        settings.max_position + settings.position_step / 2,
        settings.position_step / bin_size,
    )

    # determine the ideal potential energy at each projected spot
    potential_ideal = np.asarray(
        get_ideal_potential(time=time, positions=positions_fine)
    )
    potential_ideal_course = np.asarray(
        get_ideal_potential(time=time, positions=settings.projected_spots)
    )

    # calculate the optical field that would result from raw object data
    potential_raw = get_potential_from_weights(
        weights=potential_ideal_course, positions=positions_fine
    )
    # bin them up and find the local maximum
    potential_ideal_binned = np.asarray(potential_ideal).reshape(
        int(len(list(potential_raw)) / bin_size), bin_size
    )
    potential_raw_binned = np.asarray(potential_raw).reshape(
        int(len(list(potential_raw)) / bin_size), bin_size
    )
    # scale local optical potential to get close to the ideal value
    maxes_ideal = np.asarray([np.max(x) for x in potential_ideal_binned])
    maxes_raw = np.asarray([np.max(x) for x in potential_raw_binned])
    scalings = np.divide(
        maxes_ideal,
        maxes_raw,
        where=maxes_raw != 0.0,
        out=np.zeros_like(maxes_ideal, dtype=np.float64),
    )
    return list(np.multiply(scalings, potential_ideal_course))


def get_actual_potential(
    get_ideal_potential: Callable[[float], list],
    time: float = 0.0,
    positions: list = settings.projected_spots,
) -> list[float]:
    """Method to calculate the "actual" potential energy vs position for optical
    objects/fields as realized by the Oqtant projection system. Includes effects,
    and first-order corrections for, finite time updates and finite optical
    resolution/optical objects being projected as sums of gaussians and energetic
    clipping of optical potentials

    Args:
        get_ideal_potential (Callable[[float], list]): Object method for request/ideal potential
        time (float, optional): Time to evaluate ideal potential
        positions (list[float], optional): Positions to evaluate the actual potential at

    Returns:
        list[float]: Expected actual potential energy at the request positions
    """
    weights = get_corrected_projection_weights(
        get_ideal_potential, time=resolve_time(time)
    )

    corrected_potential = get_potential_from_weights(
        weights=weights,
        positions=positions,
    )
    return list(np.clip(np.asarray(corrected_potential), 0.0, settings.max_energy))


def gaussian(
    xs: np.ndarray,
    amp: float = 1.0,
    center: float = 0.0,
    sigma: float = 1.0,
    offset: float = 0.0,
) -> np.ndarray:
    """Method that evaluates a standard gaussian form over the given input points

    Args:
        xs (numpy.ndarray): Positions where the gaussian should be evaluated
        amp (float, optional): Gaussian amplitude
        center (float, optional): Gaussian center
        sigma (float, optional): Gaussian width
        offset (float, optional): Gaussian dc offset

    Returns:
        np.ndarray: Gaussian function evaluated over the input points
    """
    return amp * np.exp(-((xs - center) ** 2) / (2 * sigma**2)) + offset
