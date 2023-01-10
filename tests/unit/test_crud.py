import pytest

from chatbot_api.crud import (
    create_user_input,
    delete_user_input_by_dialogue_id,
    read_customer_inputs,
    read_customer_inputs_by_customer_id,
    read_customer_inputs_by_dialogue_id,
    read_customer_inputs_by_language,
    read_customer_inputs_by_customer_id_and_language,
)
from chatbot_api.models import CustomerInputs
from chatbot_api.schemas import CompleteCustomerInput, SupportedLanguages


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
def test_create_user_input(db, test_records):
    customer_input = {
        "customer_id": 111,
        "dialogue_id": 222,
        "text": "foo bar baz",
        "language": "EN"
    }
    customer_input = CompleteCustomerInput(**customer_input)
    db_customer_input = create_user_input(db, customer_input)

    expected_db_customer_input = {
        "id": 4,
        "customer_id": 111,
        "dialogue_id": 222,
        "text": "foo bar baz",
        "language": "EN"
    }
    expected_db_customer_input = CustomerInputs(**expected_db_customer_input)
    assert db_customer_input.as_dict() == expected_db_customer_input.as_dict()

    records = db.query(CustomerInputs).all()
    assert len(records) == 4
    assert records[-1].as_dict() == expected_db_customer_input.as_dict()


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
                "customer_id": 125,
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
def test_delete_user_inputs_by_dialogue_id(db, test_records):
    dialogue_id = 334
    delete_user_input_by_dialogue_id(db, dialogue_id)

    expected_db_customer_input = {
            "id": 1,
            "customer_id": 123,
            "dialogue_id": 321,
            "language": "EN",
            "text": "foo",
        }

    records = db.query(CustomerInputs).all()
    assert len(records) == 1
    assert records[0].as_dict() == expected_db_customer_input


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
def test_read_user_inputs(db, test_records):
    expected_db_customer_inputs = [
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
    ]
    db_customer_inputs = read_customer_inputs(db)
    db_customer_inputs = [input_.as_dict() for input_ in db_customer_inputs]

    assert len(db_customer_inputs) == 3
    assert db_customer_inputs == expected_db_customer_inputs


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
                "customer_id": 122,
                "dialogue_id": 322,
                "language": "FR",
                "text": "bar",
            },
            {
                "customer_id": 122,
                "dialogue_id": 334,
                "language": "IT",
                "text": "baz",
            },
            {
                "customer_id": 125,
                "dialogue_id": 336,
                "language": "FR",
                "text": "John Doe",
            },
        ],
    ],
)
def test_read_user_inputs_by_customer_id(db, test_records):
    customer_id = 122
    expected_db_customer_inputs = [
        {
            "id": 3,
            "customer_id": 122,
            "dialogue_id": 334,
            "language": "IT",
            "text": "baz",
        },
        {
            "id": 2,
            "customer_id": 122,
            "dialogue_id": 322,
            "language": "FR",
            "text": "bar",
        },
    ]
    db_customer_inputs = read_customer_inputs_by_customer_id(db, customer_id)
    db_customer_inputs = [input_.as_dict() for input_ in db_customer_inputs]

    assert len(db_customer_inputs) == 2
    assert db_customer_inputs == expected_db_customer_inputs


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
                "customer_id": 122,
                "dialogue_id": 322,
                "language": "FR",
                "text": "bar",
            },
            {
                "customer_id": 122,
                "dialogue_id": 321,
                "language": "IT",
                "text": "baz",
            },
            {
                "customer_id": 125,
                "dialogue_id": 336,
                "language": "FR",
                "text": "John Doe",
            },
        ],
    ],
)
def test_read_user_inputs_by_dialogue_id(db, test_records):
    dialogue_id = 321
    expected_db_customer_inputs = [
        {
            "id": 3,
            "customer_id": 122,
            "dialogue_id": 321,
            "language": "IT",
            "text": "baz",
        },
        {
            "id": 1,
            "customer_id": 123,
            "dialogue_id": 321,
            "language": "EN",
            "text": "foo",
        },
    ]
    db_customer_inputs = read_customer_inputs_by_dialogue_id(db, dialogue_id)
    db_customer_inputs = [input_.as_dict() for input_ in db_customer_inputs]

    assert len(db_customer_inputs) == 2
    assert db_customer_inputs == expected_db_customer_inputs


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
                "customer_id": 122,
                "dialogue_id": 322,
                "language": "FR",
                "text": "bar",
            },
            {
                "customer_id": 122,
                "dialogue_id": 334,
                "language": "IT",
                "text": "baz",
            },
            {
                "customer_id": 125,
                "dialogue_id": 336,
                "language": "FR",
                "text": "John Doe",
            },
        ],
    ],
)
def test_read_user_inputs_by_language(db, test_records):
    language = SupportedLanguages.french
    expected_db_customer_inputs = [
        {
            "id": 4,
            "customer_id": 125,
            "dialogue_id": 336,
            "language": "FR",
            "text": "John Doe",
        },
        {
            "id": 2,
            "customer_id": 122,
            "dialogue_id": 322,
            "language": "FR",
            "text": "bar",
        },
    ]
    db_customer_inputs = read_customer_inputs_by_language(db, language)
    db_customer_inputs = [input_.as_dict() for input_ in db_customer_inputs]

    assert len(db_customer_inputs) == 2
    assert db_customer_inputs == expected_db_customer_inputs


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
                "customer_id": 122,
                "dialogue_id": 322,
                "language": "FR",
                "text": "bar",
            },
            {
                "customer_id": 122,
                "dialogue_id": 334,
                "language": "IT",
                "text": "baz",
            },
            {
                "customer_id": 125,
                "dialogue_id": 336,
                "language": "FR",
                "text": "John Doe",
            },
        ],
    ],
)
def test_read_user_inputs_by_customer_id_language(db, test_records):
    customer_id = 122
    language = SupportedLanguages.french
    expected_db_customer_inputs = [
        {
            "id": 2,
            "customer_id": 122,
            "dialogue_id": 322,
            "language": "FR",
            "text": "bar",
        },
    ]
    db_customer_inputs = read_customer_inputs_by_customer_id_and_language(
        db,
        customer_id,
        language
    )
    db_customer_inputs = [input_.as_dict() for input_ in db_customer_inputs]

    assert len(db_customer_inputs) == 1
    assert db_customer_inputs == expected_db_customer_inputs
