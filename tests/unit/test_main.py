import pytest

from chatbot_api.models import CustomerInputs
from chatbot_api.schemas import SupportedLanguages


def test_get_customer_consent_inexistent_dialogue_id(test_client):
    dialogue_id = 543
    customer_input = {
        "consent": "true",
    }

    response = test_client.post(
        f"/consents/{dialogue_id}",
        json=customer_input
    )

    expected_response_json = {
        "error": f"Dialogue id {dialogue_id} does not "
                 f"exist int the current session!"
    }

    assert response.status_code == 404
    assert response.json() == expected_response_json


@pytest.mark.parametrize(
    "records",
    [
        [
            {
                "customer_id": 123,
                "dialogue_id": 321,
                "language": "EN",
                "text": "foo",
            },
            {
                "customer_id": 124,
                "dialogue_id": 334,
                "language": "FR",
                "text": "bar",
            },
            {
                "customer_id": 124,
                "dialogue_id": 334,
                "language": "IT",
                "text": "baz",
            },
{
                "customer_id": 127,
                "dialogue_id": 336,
                "language": "IT",
                "text": "baz",
            },
        ],
    ],
)
def test_get_customer_consent_false(db, test_client, test_records):
    dialogue_id = 334
    customer_input = {
        "consent": False,
    }

    response = test_client.post(
        f"/consents/{dialogue_id}",
        json=customer_input
    )

    expected_response_json = {
        "consent": False,
        "dialogue_id": dialogue_id,
    }

    assert response.status_code == 200
    assert response.json() == expected_response_json

    records = db.query(CustomerInputs) \
                .filter(CustomerInputs.dialogue_id == dialogue_id) \
                .all()

    assert len(records) == 0


@pytest.mark.parametrize(
    "records",
    [
        [
            {
                "customer_id": 123,
                "dialogue_id": 321,
                "language": "EN",
                "text": "foo",
            },
            {
                "customer_id": 124,
                "dialogue_id": 334,
                "language": "FR",
                "text": "bar",
            },
            {
                "customer_id": 124,
                "dialogue_id": 334,
                "language": "IT",
                "text": "baz",
            },
{
                "customer_id": 127,
                "dialogue_id": 336,
                "language": "IT",
                "text": "baz",
            },
        ],
    ],
)
def test_get_customer_consent_true(db, test_client, test_records):
    dialogue_id = 334
    customer_input = {
        "consent": True,
    }

    response = test_client.post(
        f"/consents/{dialogue_id}",
        json=customer_input
    )

    expected_response_json = {
        "consent": True,
        "dialogue_id": dialogue_id,
    }

    assert response.status_code == 201
    assert response.json() == expected_response_json

    records = db.query(CustomerInputs) \
                .filter(CustomerInputs.dialogue_id == dialogue_id) \
                .all()

    assert len(records) == 2


@pytest.mark.parametrize(
    "records",
    [
        [
            {
                "customer_id": 123,
                "dialogue_id": 321,
                "language": "EN",
                "text": "foo",
            },
            {
                "customer_id": 124,
                "dialogue_id": 334,
                "language": "FR",
                "text": "bar",
            },
            {
                "customer_id": 124,
                "dialogue_id": 334,
                "language": "IT",
                "text": "baz",
            },
        ],
    ],
)
def test_get_customer_input(db, test_client, test_records):
    customer_id = 456
    dialogue_id = 543
    language = SupportedLanguages.french

    customer_input = {
        "text": "foo bar baz",
        "language": language.english,
    }

    response = test_client.post(
        f"/data/{customer_id}/{dialogue_id}",
        json=customer_input
    )

    expected_response_json = {
        "customer_id": 456,
        "dialogue_id": 543,
        "text": "foo bar baz",
        "language": "EN",
    }

    assert response.status_code == 200
    assert response.json() == expected_response_json

    # Check that it does not save to db without consent.
    records = db.query(CustomerInputs).all()
    records = [record.as_dict() for record in records]

    expected_response_json.update({"id": 4})

    assert len(records) == 4
    assert expected_response_json in records


@pytest.mark.parametrize(
    "records",
    [
        [
            {
                "customer_id": 123,
                "dialogue_id": 321,
                "language": "EN",
                "text": "foo",
            },
            {
                "customer_id": 124,
                "dialogue_id": 322,
                "language": "FR",
                "text": "bar",
            },
            {
                "customer_id": 124,
                "dialogue_id": 334,
                "language": "IT",
                "text": "baz",
            },
        ],
    ],
)
def test_serve_customer_inputs(test_client, test_records):
    response = test_client.get(f"/data")

    expected_response_json = {
        "results_number": 3,
        "results": [
            {
                "id": 3,
                "customer_id": 124,
                "dialogue_id": 334,
                "language": "IT",
                "text": "baz",
            },
            {
                "id": 2,
                "customer_id": 124,
                "dialogue_id": 322,
                "language": "FR",
                "text": "bar",
            },
            {
                "id": 1,
                "customer_id": 123,
                "dialogue_id": 321,
                "language": "EN",
                "text": "foo",
            },
        ],
    }

    assert response.status_code == 200
    assert response.json() == expected_response_json


@pytest.mark.parametrize(
    "records",
    [
        [
            {
                "customer_id": 123,
                "dialogue_id": 321,
                "language": "EN",
                "text": "foo",
            },
            {
                "customer_id": 124,
                "dialogue_id": 322,
                "language": "FR",
                "text": "bar",
            },
            {
                "customer_id": 124,
                "dialogue_id": 334,
                "language": "IT",
                "text": "baz",
            },
        ],
    ],
)
def test_serve_customer_inputs_by_customer_id(test_client, test_records):
    customer_id = 124
    response = test_client.get(f"/data/?customer_id={customer_id}")

    expected_response_json = {
        "results_number": 2,
        "results": [
            {
                "id": 3,
                "customer_id": 124,
                "dialogue_id": 334,
                "language": "IT",
                "text": "baz",
            },
            {
                "id": 2,
                "customer_id": 124,
                "dialogue_id": 322,
                "language": "FR",
                "text": "bar",
            },
        ],
    }

    assert response.status_code == 200
    assert response.json() == expected_response_json


@pytest.mark.parametrize(
    "records",
    [
        [
            {
                "customer_id": 123,
                "dialogue_id": 321,
                "language": "EN",
                "text": "foo",
            },
            {
                "customer_id": 124,
                "dialogue_id": 322,
                "language": "FR",
                "text": "bar",
            },
            {
                "customer_id": 124,
                "dialogue_id": 334,
                "language": "IT",
                "text": "baz",
            },
            {
                "customer_id": 128,
                "dialogue_id": 336,
                "language": "EN",
                "text": "Jon Doe",
            },
        ],
    ],
)
def test_serve_customer_inputs_by_language(test_client, test_records):
    language = "EN"
    response = test_client.get(f"/data/?language={language}")

    expected_response_json = {
        "results_number": 2,
        "results": [
            {
                "id": 4,
                "customer_id": 128,
                "dialogue_id": 336,
                "language": "EN",
                "text": "Jon Doe",
            },
            {
                "id": 1,
                "customer_id": 123,
                "dialogue_id": 321,
                "language": "EN",
                "text": "foo",
            },
        ],
    }

    assert response.status_code == 200
    assert response.json() == expected_response_json


@pytest.mark.parametrize(
    "records",
    [
        [
            {
                "customer_id": 123,
                "dialogue_id": 321,
                "language": "EN",
                "text": "foo",
            },
            {
                "customer_id": 124,
                "dialogue_id": 322,
                "language": "FR",
                "text": "bar",
            },
            {
                "customer_id": 124,
                "dialogue_id": 334,
                "language": "IT",
                "text": "baz",
            },
            {
                "customer_id": 128,
                "dialogue_id": 336,
                "language": "EN",
                "text": "Jon Doe",
            },
        ],
    ],
)
def test_serve_customer_inputs_by_customer_id_and_language(test_client, test_records):
    customer_id = 123
    language = "EN"
    response = test_client.get(f"/data/?customer_id={customer_id}&language={language}")

    expected_response_json = {
        "results_number": 1,
        "results": [
            {
                "id": 1,
                "customer_id": 123,
                "dialogue_id": 321,
                "language": "EN",
                "text": "foo",
            },
        ],
    }

    assert response.status_code == 200
    assert response.json() == expected_response_json
