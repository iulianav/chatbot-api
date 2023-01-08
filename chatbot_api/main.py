from typing import Optional

from fastapi import Depends, FastAPI
from sqlalchemy import desc
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import CustomerInputs
from .schemas import (
    CompleteCustomerInput,
    CustomerConsent,
    CustomerInput,
    SupportedLanguages,
)

# TODO: Use Redis as cache in the future.
inputs = {}

Base.metadata.create_all(bind=engine)

description = """
API used by data scientists to further improve an existing chatbot.

Requests are sent by a background job which pushes the customer data
and consent via HTTP.
"""

app = FastAPI(
    title="Data API",
    description=description,
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.post(
    "/data/{customer_id}/{dialogue_id}",
    response_model=CompleteCustomerInput,
)
def get_customer_input(
        customer_id: int,
        dialogue_id: int,
        customer_input: CustomerInput,
):
    full_customer_input = CompleteCustomerInput(
        **customer_input.dict(),
        customer_id=customer_id,
        dialogue_id=dialogue_id
    )

    if dialogue_id in inputs:
        inputs[dialogue_id].append(full_customer_input)
    else:
        inputs[dialogue_id] = [full_customer_input]

    return full_customer_input.dict()


@app.post("/consents/{dialogue_id}")
def get_customer_consent(
        dialogue_id: int,
        consent: CustomerConsent,
        db: Session = Depends(get_db),
):
    if dialogue_id not in inputs:
        return {
            "Error": (
                f"Dialogue id {dialogue_id} does not"
                f"exist int the current session!"
            )
        }

    if consent.answer:
        for input_ in inputs[dialogue_id]:
            new_customer_input = CustomerInputs(**input_.dict())
            db.add(new_customer_input)
            db.commit()
            db.refresh(new_customer_input)

    del inputs[dialogue_id]

    return {
        "dialogue_id": dialogue_id,
        "Saved data": consent.answer,
    }


@app.get("/data")
def serve_customer_inputs(
        language: Optional[SupportedLanguages] = None,
        customer_id: Optional[int] = None,
        db: Session = Depends(get_db),
):
    query = db.query(CustomerInputs)
    if language is not None and customer_id is not None:
        query = query.filter(CustomerInputs.language == language) \
            .filter(CustomerInputs.customer_id == customer_id)
    elif language is not None:
        query = query.filter(CustomerInputs.language == language)
    elif customer_id is not None:
        query = query.filter(CustomerInputs.customer_id == customer_id)

    results = query.order_by(desc(CustomerInputs.created_at)).all()

    return {
        "status": "Success!",
        "results": len(results),
        "data": results
    }
