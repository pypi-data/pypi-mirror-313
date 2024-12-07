from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from plutous.trade.enums import AssetType, StrategyDirection, StrategyType

from .base import Base, Enum

if TYPE_CHECKING:
    from .bot import Bot


class Strategy(Base):
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    type: Mapped[StrategyType] = mapped_column(Enum(StrategyType))
    asset_type: Mapped[AssetType] = mapped_column(Enum(AssetType))
    direction: Mapped[StrategyDirection] = mapped_column(Enum(StrategyDirection))

    bots: Mapped[list["Bot"]] = relationship("Bot", back_populates="strategy")
