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

from collections import namedtuple

import pytest

from .job import *


@pytest.fixture
def job_fixtures(
    post_bec_job,
    post_barrier_job,
    post_paint1d_job,
    pending_bec_job,
    running_bec_job,
    complete_bec_job,
    complete_barrier_job,
    complete_paint_1d_job,
    failed_bec_job,
    post_bec_batch_job,
    pending_bec_batch_job,
    running_bec_batch_job,
    complete_bec_batch_job,
    failed_bec_batch_job,
):
    JobFixtures = namedtuple(
        "JobFixtures",
        [
            "post_bec_job",
            "post_barrier_job",
            "post_paint1d_job",
            "pending_bec_job",
            "running_bec_job",
            "complete_bec_job",
            "complete_barrier_job",
            "complete_paint_1d_job",
            "failed_bec_job",
            "post_bec_batch_job",
            "pending_bec_batch_job",
            "running_bec_batch_job",
            "complete_bec_batch_job",
            "failed_bec_batch_job",
        ],
    )
    yield JobFixtures(
        post_bec_job,
        post_barrier_job,
        post_paint1d_job,
        pending_bec_job,
        running_bec_job,
        complete_bec_job,
        complete_barrier_job,
        complete_paint_1d_job,
        failed_bec_job,
        post_bec_batch_job,
        pending_bec_batch_job,
        running_bec_batch_job,
        complete_bec_batch_job,
        failed_bec_batch_job,
    )
