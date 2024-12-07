from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from plutous.app.utils.session import get_session
from plutous.trade.models import ApiKey, Bot, Position, Strategy, Trade

from .models import ApiKeyPost, BotGet, BotPatch, BotPost, StrategyPost

app = FastAPI(
    title="Plutous Trade API",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    from plutous.trade.crypto.app.main import app as crypto

    app.mount("/crypto", crypto)
except ImportError:
    pass


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/strategy", response_model=StrategyPost)
def create_strategy(
    strategy: StrategyPost,
    session: Session = Depends(get_session),
) -> StrategyPost:
    session.add(Strategy(**strategy.model_dump()))
    session.commit()
    return strategy


@app.post("/api_key", response_model=ApiKeyPost)
def create_api_key(
    api_key: ApiKeyPost,
    session: Session = Depends(get_session),
) -> ApiKeyPost:
    session.add(ApiKey(**api_key.model_dump()))
    session.commit()
    return api_key


@app.get("/bot", response_model=list[BotGet])
def list_bot(
    session: Session = Depends(get_session),
) -> list[BotGet]:
    bots = session.query(Bot).all()
    return [BotGet(**bot.dict()) for bot in bots]


@app.get("/bot/{bot_id}", response_model=BotGet)
def get_bot(
    bot_id: int,
    session: Session = Depends(get_session),
) -> BotGet:
    bot = session.query(Bot).filter(Bot.id == bot_id).one()
    return BotGet(**bot.dict())


@app.post("/bot", response_model=BotPost)
def create_bot(
    bot_post: BotPost,
    session: Session = Depends(get_session),
) -> BotPost:
    session.add(
        Bot(
            sentry_dsn=str(bot_post.sentry_dsn),
            initial_capital=bot_post.allocated_capital,
            **bot_post.model_dump(exclude={"sentry_dsn"})
        )
    )
    session.commit()
    return bot_post


@app.patch("/bot/{bot_id}", response_model=BotPatch)
def update_bot(
    bot_id: int,
    bot_patch: BotPatch,
    session: Session = Depends(get_session),
) -> BotPatch:
    bot = session.query(Bot).filter(Bot.id == bot_id).first()

    for key, value in bot_patch.model_dump().items():
        if value is not None:
            setattr(bot, key, value)
            if key == "allocated_capital":
                bot.initial_capital = value
    session.commit()
    return bot_patch


@app.delete("/bot/{bot_id}")
def delete_bot(
    bot_id: int,
    session: Session = Depends(get_session),
):
    session.query(Trade).filter(
        Trade.position_id == Position.id, Position.bot_id == bot_id
    ).delete(synchronize_session=False)
    session.query(Position).filter(Position.bot_id == bot_id).delete(
        synchronize_session=False
    )
    session.query(Bot).filter(Bot.id == bot_id).delete(synchronize_session=False)
    session.commit()
    return {"message": "Bot deleted"}
