#!/home/rsm/projects/tgscheduler/venv/bin/python3

import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler
from random import choice
from pathlib import Path
from time import gmtime

from dotenv import dotenv_values
from sqlalchemy import create_engine, func, select, update
from sqlalchemy.orm import Session
from telegram import Bot

from models import Content

BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / "bot_data.db"
img_dir = BASE_DIR / "images"
conn_str = "sqlite:///" + str(db_path)
engine = create_engine(conn_str)
creds = dotenv_values(BASE_DIR / ".env")
bot_token = creds["bot_token"]
chat_id = creds["sender_chat_id"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = TimedRotatingFileHandler(
    filename=BASE_DIR / "sender.log",
    when="W0",      # Rotate every week (W0 = Monday)
    interval=1,     # Every 1 week
    backupCount=52, # Keep last N weeks of logs
)
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s:%(name)s:%(levelname)s:%(message)s",
)
logging.Formatter.converter = gmtime
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


async def send_post():
    with Session(engine) as session:
        bot = Bot(bot_token)
        
        # Get minimal count.
        stmt = select(func.min(Content.used_count))
        min_count = session.scalar(stmt)
        
        # Return ids with minimal count.
        stmt = ( 
            select(Content.id)
            .where(Content.used_count == min_count)
        )   
        available_ids = session.scalars(stmt).all()
        rand_id = choice(available_ids)
        record = session.get(Content, rand_id)
        caption = record.message
        file_id = record.img_id

        if file_id:
            # Send image with optional caption.
            image_path = img_dir / (file_id + ".jpg")

            await bot.send_photo(
                chat_id=chat_id,
                photo=image_path.open("rb"),
                caption=caption,
            )
        else:
            # Send text only.
            await bot.send_message(
                chat_id=chat_id,
                text=caption,
            )

        # Mark record as used.
        record.used_count = (record.used_count or 0) + 1
        session.commit()
        logger.info("Sent record id: %s.", record.id)


if __name__ == "__main__":
    logger.info("START sender.py")
    asyncio.run(send_post())

