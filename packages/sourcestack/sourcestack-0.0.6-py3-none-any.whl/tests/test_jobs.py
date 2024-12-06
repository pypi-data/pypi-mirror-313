import pytest
import responses
from requests import Session

from sourcestack.jobs import Jobs


@pytest.fixture
def jobs() -> Jobs:
    session = Session()
    return Jobs(base_url="https://api.sourcestack.co", session=session)


MOCK_JSON = [
    {"id": 1, "name": "Job #1"},
    {"id": 2, "name": "Job #2"},
]


@responses.activate
def test_jobs_all(jobs: Jobs):
    responses.add(
        responses.GET,
        "https://api.sourcestack.co/jobs",
        json=MOCK_JSON,
        status=200,
    )

    assert jobs.all() == MOCK_JSON


@responses.activate
def test_jobs_by_name(jobs: Jobs):
    responses.add(
        responses.GET,
        "https://api.sourcestack.co/jobs?name=Fake&exact=false",
        json=MOCK_JSON,
        status=200,
    )

    assert jobs.by_name(name="Fake") == MOCK_JSON


@responses.activate
def test_jobs_by_parent(jobs: Jobs):
    responses.add(
        responses.GET,
        "https://api.sourcestack.co/jobs?parent=Fake",
        json=MOCK_JSON,
        status=200,
    )

    assert jobs.by_parent(parent="Fake") == MOCK_JSON


@responses.activate
def test_jobs_by_url(jobs: Jobs):
    responses.add(
        responses.GET,
        "https://api.sourcestack.co/jobs?url=Fake",
        json=MOCK_JSON,
        status=200,
    )

    assert jobs.by_url(url="Fake") == MOCK_JSON


@responses.activate
def test_jobs_by_uses_product(jobs: Jobs):
    responses.add(
        responses.GET,
        "https://api.sourcestack.co/jobs?uses_product=Fake&exact=false",
        json=MOCK_JSON,
        status=200,
    )

    assert jobs.by_uses_product(uses_product="Fake", exact=False) == MOCK_JSON


@responses.activate
def test_jobs_by_uses_category(jobs: Jobs):
    responses.add(
        responses.GET,
        "https://api.sourcestack.co/jobs?uses_category=Fake&exact=false",
        json=MOCK_JSON,
        status=200,
    )

    assert jobs.by_uses_category(uses_category="Fake", exact=False) == MOCK_JSON
