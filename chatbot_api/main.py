from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


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


class SupportedLanguages(str, Enum):
    english = "EN"
    french = "FR"
    german = "GE"
    italian = "IT"


class CustomerInput(BaseModel):
    text: str
    language: SupportedLanguages


class CustomerConsent(BaseModel):
    answer: bool


@app.post("/data/{customer_id}/{dialogue_id}")
def get_customer_input(
        customer_id: int,
        dialogue_id: int,
        customer_input: CustomerInput,
):
    return {
        "customer_id": customer_id,
        "dialogue_id": dialogue_id,
        "customer_input": customer_input,
    }


@app.post("/consents/{dialogue_id}")
def get_customer_consent(
        dialogue_id: int,
        consent: CustomerConsent,
):
    return {
        "dialogue_id": dialogue_id,
        "consent": consent,
    }


@app.get("/data")
def serve_customer_inputs(
        language: Optional[str] = None,
        customer_id: Optional[int] = None,
):
    return {
        "language": language,
        "customer_id": customer_id,
    }
