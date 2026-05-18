from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Alembic'in tabloyu görmesi için:
from app.models.user import User