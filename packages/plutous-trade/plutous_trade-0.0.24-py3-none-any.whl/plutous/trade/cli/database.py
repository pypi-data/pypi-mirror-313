from pathlib import Path

from typer import Typer

from plutous import database as db
from plutous.trade.models import Base

app = Typer(name="db")
directory = Path(__file__).parent.parent


@app.command()
def init():
    db.init("trade", Base.metadata, directory)


@app.command()
def revision(msg: str):
    db.revision(directory, msg)


@app.command()
def upgrade(revision: str = "head"):
    db.upgrade(directory, revision)


@app.command()
def downgrade(revision: str):
    db.downgrade(directory, revision)


@app.command()
def reset():
    db.reset("trade")
