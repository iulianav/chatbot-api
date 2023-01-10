import pytest

from chatbot_api.models import CustomerInputs


@pytest.fixture(scope="function")
def test_records(db, records):
    customer_inputs = [CustomerInputs(**record) for record in records]
    for input_ in customer_inputs:
        db.add(input_)
        db.commit()
        db.refresh(input_)
    yield
    db.query(CustomerInputs).delete()
