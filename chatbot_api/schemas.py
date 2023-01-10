from enum import Enum
from typing import List

from pydantic import BaseModel


class SupportedLanguages(str, Enum):
    english = "EN"
    french = "FR"
    german = "GE"
    italian = "IT"


class CustomerInput(BaseModel):
    text: str
    language: SupportedLanguages


class CompleteCustomerInput(CustomerInput):
    customer_id: int
    dialogue_id: int


class CustomerConsent(BaseModel):
    consent: bool


class CustomerConsentResponse(CustomerConsent):
    dialogue_id: int


class DatabaseCustomerInputRecord(CompleteCustomerInput):
    id: int


class CustomerInputResponse(BaseModel):
    results_number: int
    results: List[DatabaseCustomerInputRecord]


class Error(BaseModel):
    error: str
