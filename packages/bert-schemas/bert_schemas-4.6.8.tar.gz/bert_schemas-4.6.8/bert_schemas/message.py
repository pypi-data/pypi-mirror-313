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

from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class MessageBase(BaseModel):
    location: int = 1
    message: str
    start_datetime: datetime
    end_datetime: datetime
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)


class Message(MessageBase):
    id: int


class MessageResponse(Message):
    location: int = 1
    message: str
    start_datetime: str | datetime
    end_datetime: str | datetime

    @field_validator("start_datetime", mode="before")
    @classmethod
    def formate_start_datetime(cls, value):
        return value.strftime("%m/%d/%Y @ %H:%M")

    @field_validator("end_datetime", mode="before")
    @classmethod
    def formate_end_datetime(cls, value):
        return value.strftime("%m/%d/%Y @ %H:%M")
