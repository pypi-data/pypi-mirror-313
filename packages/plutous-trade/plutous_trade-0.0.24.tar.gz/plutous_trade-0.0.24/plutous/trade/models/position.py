from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from plutous.enums import Exchange
from plutous.trade.enums import AssetType, PositionSide

from .base import Base, Enum
from .bot import Bot

if TYPE_CHECKING:
    from .trade import Trade


class Position(Base):
    asset_type: Mapped[AssetType] = mapped_column(Enum(AssetType))
    exchange: Mapped[Exchange] = mapped_column(Enum(Exchange, schema="public"))
    symbol: Mapped[str]
    side: Mapped[PositionSide] = mapped_column(Enum(PositionSide))
    price: Mapped[Decimal] = mapped_column(DECIMAL(20, 8))
    quantity: Mapped[Decimal] = mapped_column(DECIMAL(20, 8))
    realized_pnl: Mapped[Decimal] = mapped_column(DECIMAL(20, 8))
    opened_at: Mapped[datetime]
    closed_at: Mapped[Optional[datetime]]
    bot_id: Mapped[int] = mapped_column(ForeignKey(Bot.id))

    bot: Mapped[Bot] = relationship(Bot, back_populates="positions")
    trades: Mapped[list["Trade"]] = relationship("Trade", back_populates="position")
