from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase


class DatabaseModel(DeclarativeBase):
    """SQLAlchemy model.

    Fields:

        id - Primary key.

        deleted_at - Datetime when row was deleted.

    """

    id: Column
    deleted_at: Column

    @classmethod
    def field_by_name(cls, name: str) -> Column:
        """Returns sqlalchemy model Column by name."""

        raise NotImplementedError
