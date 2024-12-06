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

"""Pytest fixtures for jobs"""

import pytest

from ..factories.helpers import add_notes, set_run
from ..factories import job as JobFactories
from collections import namedtuple


@pytest.fixture
def post_bec_job():
    job = JobFactories.BecJobPostFactory.build()
    yield job


@pytest.fixture
def post_barrier_job():
    job = JobFactories.BarrierJobPostFactory.build()
    yield job


@pytest.fixture
def post_paint1d_job():
    job = JobFactories.Paint1dJobPostFactory.build()
    yield job


@pytest.fixture
def pending_bec_job():
    job = JobFactories.BecJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    yield job


@pytest.fixture
def running_bec_job():
    job = JobFactories.BecJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    yield job


@pytest.fixture
def complete_bec_job():
    job = JobFactories.BecJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    yield job


@pytest.fixture
def complete_barrier_job():
    job = JobFactories.BarrierJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    yield job


@pytest.fixture
def complete_paint_1d_job():
    job = JobFactories.Paint1dJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    yield job


@pytest.fixture
def failed_bec_job():
    job = JobFactories.BecJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    yield job


@pytest.fixture
def post_bec_batch_job():
    job = JobFactories.BecBatchJobPostFactory.build()
    yield job


@pytest.fixture
def pending_bec_batch_job():
    job = JobFactories.BecBatchJobPendingFactory.build()
    job = add_notes(job)
    job = set_run(job)
    yield job


@pytest.fixture
def running_bec_batch_job():
    job = JobFactories.BecBatchJobRunningFactory.build()
    job = add_notes(job)
    job = set_run(job)
    yield job


@pytest.fixture
def complete_bec_batch_job():
    job = JobFactories.BecBatchJobCompleteFactory.build()
    job = add_notes(job)
    job = set_run(job)
    yield job


@pytest.fixture
def failed_bec_batch_job():
    job = JobFactories.BecBatchJobFailedFactory.build()
    job = add_notes(job)
    job = set_run(job)
    yield job


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
