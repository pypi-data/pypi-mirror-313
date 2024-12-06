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

"""Helper functions for pydantic factories"""

# from ..schemas.job import BertJobSchema


def get_input_count(_, values: dict) -> int:
    return len(values["inputs"])


def add_notes(job):
    for number, input in enumerate(job.inputs):
        input.notes = f"test {job.job_type.lower()} note #{number + 1}"
    return job


def set_run(job):
    for i, input in enumerate(job.inputs):
        input.run = i + 1
    return job
