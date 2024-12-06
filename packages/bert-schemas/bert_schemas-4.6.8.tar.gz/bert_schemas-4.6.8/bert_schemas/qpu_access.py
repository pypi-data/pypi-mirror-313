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

from datetime import date, time
from enum import Enum

from pydantic import BaseModel

from bert_schemas import qpu


class DayOfWeek(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

    def __str__(self):
        return str(self.value)


class AccessType(str, Enum):
    GROUP = "GROUP"
    ROLE = "ROLE"
    ORG = "ORG"
    QPU = "QPU"

    def __str__(self):
        return str(self.value)


class AccessSlot(BaseModel):
    day: DayOfWeek
    start_date: date
    end_date: date | None = None
    start_time: time
    end_time: time


class Access(BaseModel):
    qpu_name: qpu.QPUName
    access_name: str | None = None
    access_type: AccessType
    access_slots: list[AccessSlot] = []
