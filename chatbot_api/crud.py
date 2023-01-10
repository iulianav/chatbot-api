from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from .models import CustomerInputs
from .schemas import CompleteCustomerInput, SupportedLanguages


def create_user_input(
        db: Session,
        customer_input: CompleteCustomerInput,
) -> CustomerInputs:
    new_customer_input = CustomerInputs(**customer_input.dict())
    db.add(new_customer_input)
    db.commit()
    db.refresh(new_customer_input)
    return new_customer_input


def delete_user_input_by_dialogue_id(
        db: Session,
        dialogue_id: int,
) -> None:
    db.query(CustomerInputs) \
       .filter(CustomerInputs.dialogue_id == dialogue_id) \
       .delete()
    db.commit()
    return None


def read_customer_inputs(db: Session) -> List[CustomerInputs]:
    results = db.query(CustomerInputs).order_by(desc(CustomerInputs.id)).all()
    return results


def read_customer_inputs_by_customer_id(
        db: Session,
        customer_id: int,
) -> List[CustomerInputs]:
    results = db.query(CustomerInputs) \
                .filter(CustomerInputs.customer_id == customer_id) \
                .order_by(desc(CustomerInputs.id)) \
                .all()
    return results


def read_customer_inputs_by_dialogue_id(
        db: Session,
        dialogue_id: int,
) -> List[CustomerInputs]:
    results = db.query(CustomerInputs) \
                .filter(CustomerInputs.dialogue_id == dialogue_id) \
                .order_by(desc(CustomerInputs.id)) \
                .all()
    return results


def read_customer_inputs_by_language(
        db: Session,
        language: SupportedLanguages,
) -> List[CustomerInputs]:
    results = db.query(CustomerInputs) \
                .filter(CustomerInputs.language == language) \
                .order_by(desc(CustomerInputs.id)) \
                .all()
    return results


def read_customer_inputs_by_customer_id_and_language(
        db: Session,
        customer_id: int,
        language: SupportedLanguages,
) -> List[CustomerInputs]:
    results = db.query(CustomerInputs) \
                .filter(CustomerInputs.customer_id == customer_id) \
                .filter(CustomerInputs.language == language) \
                .order_by(desc(CustomerInputs.id)) \
                .all()
    return results
