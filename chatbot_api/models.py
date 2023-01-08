import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Integer,
    String,
)

from .database import Base
from .schemas import SupportedLanguages


class CustomerInputs(Base):
    __tablename__ = "user_inputs"

    # TODO: Use UUIDs instead of Integers.
    id = Column(Integer, primary_key=True, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # TODO: Make foreign key to "UserDialogues" table in the future.
    dialogue_id = Column(Integer, nullable=False)

    # TODO: Make foreign key to a "Users" table in the future.
    customer_id = Column(Integer, nullable=False)

    language = Column(Enum(SupportedLanguages), nullable=False)
    text = Column(String, nullable=False)
