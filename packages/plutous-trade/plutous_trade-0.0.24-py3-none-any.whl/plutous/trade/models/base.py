from sqlalchemy.orm import DeclarativeBase, declared_attr

from plutous.models.base import BaseMixin
from plutous.models.base import Enum as BaseEnum


class Base(DeclarativeBase, BaseMixin):
    @declared_attr.directive
    def __table_args__(cls) -> tuple:
        return (
            *super().__table_args__,
            {"schema": "trade"},
        )


class Enum(BaseEnum):
    schema = "trade"
