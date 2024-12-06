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

"""Pydantic factories for BEC jobs"""

from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory

from ... import job as job_schema
from ... import qpu as qpu_schema


class BarrierFactory(ModelFactory):
    __model__ = job_schema.Barrier
    shape = job_schema.ShapeType.GAUSSIAN
    times_ms = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    positions_um = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    heights_khz = [0, 20, 40, 60, 80, 100, 100, 100, 100, 100, 100]
    widths_um = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


class LandscapeFactory(ModelFactory):
    __model__ = job_schema.Landscape
    time_ms = 2.0
    potentials_khz = [1.0, 2.0, 3.0]
    positions_um = [3.0, 4.0, 5.0]


class OpticalLandscapeFactory(ModelFactory):
    __model__ = job_schema.OpticalLandscape
    landscape1 = LandscapeFactory.build()
    landscape2 = LandscapeFactory.build()
    landscape2.time_ms = 3.0
    landscapes = [landscape1, landscape2]


class OutputFactory(ModelFactory):
    __model__ = job_schema.Output


class NonPlotOutputFactory(ModelFactory):
    __model__ = job_schema.NonPlotOutput


class PlotOutputFactory(ModelFactory):
    __model__ = job_schema.PlotOutput


class BarrierOutputFactory(ModelFactory):
    __model__ = job_schema.BarrierOutput


class OutputNonPlotOutputFactory(OutputFactory):
    values = NonPlotOutputFactory.build()


class OutputPlotOutputFactory(OutputFactory):
    values = PlotOutputFactory.build()


class InputValuesFactory(ModelFactory):
    __model__ = job_schema.InputValues
    end_time_ms = 20
    image_type = "TIME_OF_FLIGHT"
    time_of_flight_ms = 6
    rf_evaporation = {
        "times_ms": [-1000.0, -500.0],
        "frequencies_mhz": [2.0, 2.0],
        "powers_mw": [3.0, 3.0],
        "interpolation": "LINEAR",
    }
    optical_barriers = None
    optical_landscape = None
    lasers = None


class BarrierInputValuesFactory(InputValuesFactory):
    optical_barriers = Use(BarrierFactory.batch, size=2)


class Paint1dInputValuesFactory(InputValuesFactory):
    optical_landscape = OpticalLandscapeFactory.build()


class InputFactory(ModelFactory):
    __model__ = job_schema.Input
    values = InputValuesFactory.build()
    run = None
    output = None
    notes = None


class InputNonPlotOutputFactory(InputFactory):
    output = OutputNonPlotOutputFactory.build()


class InputPlotOutputFactory(InputFactory):
    output = OutputPlotOutputFactory.build()


class BarrierInputFactory(InputFactory):
    values = BarrierInputValuesFactory.build()


class BarrierInputOutputFactory(BarrierInputFactory):
    output = BarrierOutputFactory.build()


class Paint1dInputFactory(InputFactory):
    values = Paint1dInputValuesFactory.build()


class BecJobPostFactory(ModelFactory):
    __model__ = job_schema.JobPost
    name = job_schema.JobName("test bec job - pending")
    qpu_name = qpu_schema.QPUName.UNDEFINED
    status = job_schema.JobStatus.PENDING
    display = True
    inputs = [InputFactory.build()]


class BarrierJobPostFactory(ModelFactory):
    __model__ = job_schema.JobPost
    name = job_schema.JobName("test barrier job - pending")
    qpu_name = qpu_schema.QPUName.UNDEFINED
    status = job_schema.JobStatus.PENDING
    display = True
    inputs = [BarrierInputFactory.build()]


class Paint1dJobPostFactory(ModelFactory):
    __model__ = job_schema.JobPost
    name = job_schema.JobName("test paint_1d job - pending")
    qpu_name = qpu_schema.QPUName.UNDEFINED
    status = job_schema.JobStatus.PENDING
    display = True
    inputs = [Paint1dInputFactory.build()]


class BecJobPendingFactory(ModelFactory):
    __model__ = job_schema.JobCreate
    name = job_schema.JobName("test bec job - pending")
    qpu_name = qpu_schema.QPUName.UNDEFINED
    status = job_schema.JobStatus.PENDING
    display = True
    inputs = [InputFactory.build()]


class BecJobRunningFactory(BecJobPendingFactory):
    name = job_schema.JobName("test bec job - running")
    status = job_schema.JobStatus.RUNNING


class BecJobCompleteFactory(ModelFactory):
    __model__ = job_schema.JobCreate
    name = job_schema.JobName("test bec job - complete")
    qpu_name = qpu_schema.QPUName.BIGBERT
    status = job_schema.JobStatus.COMPLETE
    display = True
    inputs = [InputNonPlotOutputFactory.build()]


class BarrierJobCompleteFactory(ModelFactory):
    __model__ = job_schema.JobCreate
    name = job_schema.JobName("test barrier job - complete")
    qpu_name = qpu_schema.QPUName.UNDEFINED
    status = job_schema.JobStatus.COMPLETE
    display = True
    inputs = [BarrierInputOutputFactory.build()]


class Paint1dJobCompleteFactory(ModelFactory):
    __model__ = job_schema.JobCreate
    name = job_schema.JobName("test paint_1d job - complete")
    qpu_name = qpu_schema.QPUName.UNDEFINED
    status = job_schema.JobStatus.COMPLETE
    display = True
    inputs = [BarrierInputOutputFactory.build()]


class BecJobFailedFactory(BecJobPendingFactory):
    name = job_schema.JobName("test bec job - failed")
    status = job_schema.JobStatus.FAILED


class BecBatchJobPendingFactory(BecJobPendingFactory):
    name = job_schema.JobName("test bec batch job - pending")
    inputs = Use(InputFactory.batch, size=2)


class BecBatchJobPostFactory(BecJobPostFactory):
    name = job_schema.JobName("test bec batch job - pending")
    inputs = Use(InputFactory.batch, size=2)


class BecBatchJobRunningFactory(BecBatchJobPendingFactory):
    name = job_schema.JobName("test bec batch job - running")
    status = job_schema.JobStatus.RUNNING


class BecBatchJobCompleteFactory(BecJobCompleteFactory):
    name = job_schema.JobName("test bec batch job - complete")
    inputs = Use(InputNonPlotOutputFactory.batch, size=2)


class BecBatchJobFailedFactory(BecBatchJobPendingFactory):
    name = job_schema.JobName("test bec batch job - failed")
    status = job_schema.JobStatus.FAILED
