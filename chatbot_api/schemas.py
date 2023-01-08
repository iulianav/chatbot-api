from enum import Enum

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
    answer: bool
