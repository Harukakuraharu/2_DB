import sqlalchemy as sa

from core.settings import config
from models.models import Base


def main():
    engine = sa.create_engine(config.dsn, echo=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
