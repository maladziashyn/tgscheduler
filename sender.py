import asyncio
from pathlib import Path

from dotenv import dotenv_values
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session

from telegram import Bot

from models import Content

BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / "bot_data.db"
img_dir = BASE_DIR / "images"
conn_str = "sqlite:///" + str(db_path)
engine = create_engine(conn_str)
creds = dotenv_values(BASE_DIR / ".env")


async def send_post():
    bot = Bot(creds["bot_token"])

    with Session(engine) as session:
        # Return ids with minimal count.
        stmt = (
            select(Content.id)
            .where(Content.used_count == 0)
        )
        result = session.scalars(stmt).all()

        record = session.execute(stmt).scalar_one_or_none()

        if not record:
            print("No content available")
            return
