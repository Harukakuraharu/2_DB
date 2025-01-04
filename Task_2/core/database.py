from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import config
from models.models import Base


engine = create_engine(config.dsn)
Session = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)


def initial_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
