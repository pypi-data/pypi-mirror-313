from pydantic import BaseModel, HttpUrl

from plutous.enums import Exchange
from plutous.trade.enums import AssetType, BotType, StrategyDirection, StrategyType


class StrategyPost(BaseModel):
    name: str
    description: str
    type: StrategyType
    asset_type: AssetType
    direction: StrategyDirection


class BaseBot(BaseModel):
    name: str
    strategy_id: int
    api_key_id: int
    type: BotType
    allocated_capital: float
    accumulate: bool = True
    max_position: int = 1
    alert: bool = False
    sentry_dsn: HttpUrl | None = None
    discord_webhooks: list[str] = []


class BotPost(BaseBot):
    pass


class BotGet(BaseBot):
    id: int
    initial_capital: float


class BotPatch(BaseModel):
    name: str | None = None
    strategy_id: int | None = None
    api_key_id: int | None = None
    type: BotType | None = None
    allocated_capital: float | None = None
    accumulate: bool | None = None
    max_position: int | None = None
    alert: bool | None = None
    sentry_dsn: HttpUrl | None = None
    discord_webhooks: list[str] | None = None


class ApiKeyPost(BaseModel):
    name: str
    exchange: Exchange
    key: str
    secret: str
    passphrase: str | None = None
