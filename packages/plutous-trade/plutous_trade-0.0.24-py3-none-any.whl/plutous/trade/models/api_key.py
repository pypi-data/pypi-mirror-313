from typing import TYPE_CHECKING, Optional

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship
from sqlalchemy_utils import EncryptedType

from plutous.config import CONFIG
from plutous.enums import Exchange

from .base import Base, Enum

if TYPE_CHECKING:
    from .bot import Bot


class ApiKey(Base):
    exchange: Mapped[Exchange] = mapped_column(Enum(Exchange, schema="public"))
    name: Mapped[str]
    key: Mapped[str]
    secret: Mapped[str] = mapped_column(EncryptedType(String, CONFIG.encryption_key))
    passphrase: Mapped[Optional[str]] = mapped_column(
        EncryptedType(String, CONFIG.encryption_key), nullable=True
    )
    user_token: Mapped[Optional[str]] = mapped_column(
        EncryptedType(String, CONFIG.encryption_key), nullable=True
    )

    bots: Mapped[list["Bot"]] = relationship("Bot", back_populates="api_key")

    @declared_attr.directive
    def __table_args__(cls) -> tuple:
        return (
            Index(
                f"ix_{cls.__tablename__}_exchange_name",
                "exchange",
                "name",
                unique=True,
            ),
            *super().__table_args__,
        )
