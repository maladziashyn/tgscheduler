"""Create a database, images dir, and an empty .env file."""

import shutil
from pathlib import Path

from models import Base
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent
db = BASE_DIR / "bot_data.db"
img_dir = BASE_DIR / "images"
log_dir = BASE_DIR / "log"
env_file = BASE_DIR / ".env"

def main():
    db.unlink(missing_ok=True)
    db.touch()
    engine = create_engine("sqlite:///" + str(db), echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Create images, log dir, empty .env file
    for d in [img_dir, log_dir]:
        if d.exists:
            shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True, exist_ok=True)

    with env_file.open("w") as f:
        f.write(
            "bot_token=<your_token>\n"
            "sender_chat_id=<target_chat_id>\n"
            "receiver_chat_id=<chat_with_your_bot>\n"
        )


if __name__ == "__main__":
    answer = input(
        "You're about to delete existing database, images, logs, .env, "
        "and create them as empty files/directories. Continue? (y/n): "
    ).strip().lower()
    if answer == "y":
        main()
        print("Done")
    else:
        print("Aborted")

