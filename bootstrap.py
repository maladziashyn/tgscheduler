"""Create a database, images dir, and an empty .env file."""

import shutil
from pathlib import Path

from models import Base
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent
db_path = Path(BASE_DIR / "bot_data.db")
img_dir = Path(BASE_DIR / "images")

def main():
    db_path.touch()
    engine = create_engine("sqlite:///" + str(db_path), echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Create images dir, empty .env file
    if img_dir.exists:
        shutil.rmtree(img_dir)
    img_dir.mkdir(parents=True, exist_ok=True)

    #with Path(BASE_DIR / ".env").open("w") as f:
    #    f.write("bot_token=<your_token>\nsender_chat_id=<target_chat_id>\nreceiver_chat_id=<chat_with_your_bot>")

    Path(BASE_DIR / "sender.log").unlink(missing_ok=True)
    Path(BASE_DIR / "receiver.log").unlink(missing_ok=True)

if __name__ == "__main__":
    main()

