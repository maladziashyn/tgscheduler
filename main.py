from datetime import UTC, datetime
from pathlib import Path

from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from telegram.ext import ApplicationBuilder, MessageHandler, filters

from models import Content

BASE_DIR = Path(__file__).resolve().parent
db_path = Path(BASE_DIR / "bot_data.db")
img_dir = Path(BASE_DIR / "images")
conn_str = "sqlite:///" + str(db_path)
engine = create_engine(conn_str)

creds = dotenv_values(BASE_DIR / ".env")


async def handle_text(update, context):  # noqa: ARG001
    text = update.message.text
    with Session(engine) as session:
        record = Content(message=text)
        session.add(record)
        session.commit()
        record_id = record.id

    print_me(f"added id: {record_id}")
    await update.message.reply_text(f"text saved, id {record_id}")


async def handle_photo(update, context):  # noqa: ARG001
    caption = update.message.caption
    if update.message.photo:
        doc = update.message.photo[-1]
    elif update.message.document:
        doc = update.message.document
    file = await doc.get_file()
    file_path = str(Path(img_dir / (file.file_unique_id + ".jpg")))
    await file.download_to_drive(file_path, read_timeout=30)
    with Session(engine) as session:
        record = Content(
            message=caption,
            img_id=file.file_unique_id,
        )
        session.add(record)
        session.commit()
        record_id = record.id

    print_me(f"added id: {record_id}")
    await update.message.reply_text(f"image saved, id {record_id}")


def print_me(txt):
    print(
        "\r",
        datetime.strftime(datetime.now(UTC), "%Y-%m-%d %H:%M:%S.%f")[:-3],
        txt,
        end="",
        flush=True
    )


def main():
    app = ApplicationBuilder().token(creds["bot_token"]).build()
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text,
    ))
    app.add_handler(MessageHandler(
        filters.PHOTO | filters.Document.IMAGE,
        handle_photo,
    ))
    app.run_polling()

if __name__ == "__main__":
    print_me("Started")
    main()

