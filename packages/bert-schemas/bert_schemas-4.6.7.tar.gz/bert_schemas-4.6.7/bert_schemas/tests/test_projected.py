import numpy as np

from .. import job as job_schema
from .. import projected


def test_projected_gaussian():
    xs = np.arange(-10, 10, 0.1)
    assert projected.gaussian(xs)[0] == 1.9287498479639178e-22


def test_get_potential_from_weights():
    assert projected.get_potential_from_weights(
        list(range(1, 122, 1)), [1.0, 2.2, 3.5]
    ) == [85.91219226992594, 87.25507420353789, 88.46888252900956]


def test_get_corrected_projection_weights():
    bar = job_schema.Barrier()
    res = projected.get_corrected_projection_weights(bar.get_ideal_potential, time=2.0)
    assert len(res) == 121
    assert res[30] == 1.5881403774524704e-272


def test_get_actual_potential():
    bar = job_schema.Barrier()
    res = projected.get_actual_potential(
        bar.get_ideal_potential, time=2.0, positions=[1.0, 2.2, 3.5]
    )
    assert res == [6.631842134176605, 9.772009614670178, 4.038341506097124]
