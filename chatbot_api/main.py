from typing import Optional, Union

from fastapi import Depends, FastAPI, Response, status
from sqlalchemy.orm import Session

from .crud import (
    create_user_input,
    delete_user_input_by_dialogue_id,
    read_customer_inputs,
    read_customer_inputs_by_customer_id,
    read_customer_inputs_by_language,
    read_customer_inputs_by_customer_id_and_language,
)
from .database import Base, engine, get_db
from .models import CustomerInputs
from .schemas import (
    CompleteCustomerInput,
    CustomerConsent,
    CustomerConsentResponse,
    CustomerInput,
    CustomerInputResponse,
    Error,
    SupportedLanguages,
)

# TODO: Use Redis as cache in the future instead of storing
# in DB from the start.

Base.metadata.create_all(bind=engine)

description = """
API used by data scientists to further improve an existing chatbot.

Requests are sent by a background job which pushes the customer data
and consent via HTTP.
"""

app = FastAPI(
    title="Data API",
    dependencies=[Depends(get_db)],
    description=description,
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.post("/data/{customer_id}/{dialogue_id}", status_code=status.HTTP_200_OK)
def get_customer_input(
        customer_id: int,
        dialogue_id: int,
        customer_input: CustomerInput,
        db: Session = Depends(get_db),
) -> CompleteCustomerInput:
    full_customer_input = CompleteCustomerInput(
        **customer_input.dict(),
        customer_id=customer_id,
        dialogue_id=dialogue_id,
    )

    create_user_input(db, full_customer_input)

    return full_customer_input


@app.post("/consents/{dialogue_id}", status_code=status.HTTP_200_OK)
def get_customer_consent(
        dialogue_id: int,
        response: Response,
        consent: CustomerConsent,
        db: Session = Depends(get_db),
) -> Union[CustomerConsentResponse, Error]:
    # TODO: Maybe add a boolean column `consent` to no longer retrieve
    # already consented inputs.
    dialogue_inputs = db.query(CustomerInputs) \
                        .filter(CustomerInputs.dialogue_id == dialogue_id) \
                        .all()
    if len(dialogue_inputs) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return Error(
            error=(
                f"Dialogue id {dialogue_id} does not "
                f"exist int the current session!"
            )
        )

    if consent.consent:
        response.status_code = status.HTTP_201_CREATED
    else:
        delete_user_input_by_dialogue_id(db, dialogue_id)

    return CustomerConsentResponse(
        consent=consent.consent,
        dialogue_id=dialogue_id,
    )


@app.get("/data", status_code=status.HTTP_200_OK)
def serve_customer_inputs(
        language: Optional[SupportedLanguages] = None,
        customer_id: Optional[int] = None,
        db: Session = Depends(get_db),
) -> CustomerInputResponse:
    if language is not None and customer_id is not None:
        results = read_customer_inputs_by_customer_id_and_language(
            db,
            customer_id,
            language,
        )
    elif language is not None:
        results = read_customer_inputs_by_language(
            db,
            language,
        )
    elif customer_id is not None:
        results = read_customer_inputs_by_customer_id(
            db,
            customer_id,
        )
    else:
        results = read_customer_inputs(db)

    # TODO: find a better way to convert results to dict.
    results = [res.as_dict() for res in results]

    return CustomerInputResponse(
        results_number=len(results),
        results=results,
    )
