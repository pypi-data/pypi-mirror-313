from loguru import logger
from typer import Typer

from . import database

app = Typer(name="trade")
apps = [database.app]

try:
    from plutous.trade.crypto.cli import main as crypto
    apps.append(crypto.app)
except ImportError as e:
    logger.warning(e)

for a in apps:
    app.add_typer(a)
