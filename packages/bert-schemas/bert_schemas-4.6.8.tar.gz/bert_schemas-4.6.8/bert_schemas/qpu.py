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

from datetime import time
from enum import Enum

from pydantic import BaseModel, ConfigDict


class QPUName(str, Enum):
    SMALLBERT = "SMALLBERT"
    BIGBERT = "BIGBERT"
    UNDEFINED = "UNDEFINED"
    SIMULATOR = "SIMULATOR"

    def __str__(self):
        return str(self.value)


class QPUStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    TESTING = "TESTING"

    def __str__(self):
        return str(self.value)


class QPUJobType(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class QPUAccess(BaseModel):
    day: str
    start_time: time
    end_time: time

    model_config = ConfigDict(from_attributes=True)


class QPUBase(BaseModel):
    name: QPUName
    status: QPUStatus
    model_config = ConfigDict(from_attributes=True)


class QPU(QPUBase):
    job_types: list[QPUJobType]

    model_config = ConfigDict(from_attributes=True)


class QPUState(QPU):
    pending_internal_jobs: int | None = None
    pending_external_jobs: int | None = None


class Heartbeat(BaseModel):
    time_complete: str
    atom_number: int
    condensate_fraction: int
    temperature: float


class QPUStatusUpdate(BaseModel):
    status: QPUStatus

    # @root_validator()
    # def check_status_or_hours(cls, values):
    #     if (values.get("status") is None) and (values.get("operation_hours") is None):
    #         raise ValueError("either status or operation_hours is required")
    #     return values
