"""Create a database, images dir, and an empty .env file."""

from pathlib import Path

from models import Base
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent
db_path = Path(BASE_DIR / "bot_data.db")

def main():
    db_path.touch()
    engine = create_engine("sqlite:///" + str(db_path), echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Create images dir, empty .env file
    Path(BASE_DIR / "images").mkdir(parents=True, exist_ok=True)

    with Path(BASE_DIR / ".env").open("w") as f:
        f.write("bot_token=<your_token>\n")


if __name__ == "__main__":
    main()

