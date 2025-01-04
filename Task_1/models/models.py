import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


idpk = Annotated[int, mapped_column(primary_key=True)]


class Genre(Base):
    __tablename__ = "genre"

    genre_id: Mapped[idpk]
    name_genre: Mapped[str]
    books: Mapped[list["Book"]] = relationship(
        back_populates="genres", lazy="joined"
    )


class Author(Base):
    __tablename__ = "author"

    author_id: Mapped[idpk]
    name_author: Mapped[str]
    books: Mapped[list["Book"]] = relationship(
        back_populates="authors", lazy="joined"
    )


class City(Base):
    __tablename__ = "city"

    city_id: Mapped[idpk]
    name_city: Mapped[str]
    days_delivery: Mapped[datetime.time]
    client: Mapped["Client"] = relationship(
        back_populates="city", lazy="joined"
    )


class Book(Base):
    __tablename__ = "book"

    book_id: Mapped[idpk]
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(
        ForeignKey("author.author_id", ondelete="CASCADE")
    )
    authors: Mapped[list[Author]] = relationship(
        back_populates="books", lazy="joined"
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genre.genre_id", ondelete="CASCADE")
    )
    genres: Mapped[list[Genre]] = relationship(
        back_populates="books", lazy="joined"
    )
    price: Mapped[int]
    amount: Mapped[int]
    buy_book: Mapped["BuyBook"] = relationship(
        back_populates="book", lazy="joined"
    )


class Client(Base):
    __tablename__ = "client"

    client_id: Mapped[idpk]
    name_client: Mapped[str]
    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.city_id", ondelete="CASCADE")
    )
    city: Mapped[City] = relationship(back_populates="client", lazy="joined")
    email: Mapped[str]
    buy: Mapped["Buy"] = relationship(back_populates="client", lazy="joined")


class Buy(Base):
    __tablename__ = "buy"

    buy_id: Mapped[idpk]
    buy_description: Mapped[str]
    client_id: Mapped[int] = mapped_column(
        ForeignKey("client.client_id", ondelete="CASCADE")
    )
    client: Mapped[Client] = relationship(back_populates="buy", lazy="joined")
    buy_book: Mapped["BuyBook"] = relationship(
        back_populates="buy", lazy="joined"
    )
    buy_step: Mapped["BuyStep"] = relationship(
        back_populates="buy", lazy="joined"
    )


class Step(Base):
    __tablename__ = "step"

    step_id: Mapped[idpk]
    name_step: Mapped[str]
    buy_step: Mapped["BuyStep"] = relationship(
        back_populates="step", lazy="joined"
    )


class BuyBook(Base):
    __tablename__ = "buy_book"

    buy_book_id: Mapped[idpk]
    buy_id: Mapped[int] = mapped_column(
        ForeignKey("buy.buy_id", ondelete="CASCADE"), unique=True
    )
    buy: Mapped[Buy] = relationship(back_populates="buy_book", lazy="joined")
    book_id: Mapped[int] = mapped_column(
        ForeignKey("book.book_id", ondelete="CASCADE"), unique=True
    )
    book: Mapped[Book] = relationship(back_populates="buy_book", lazy="joined")
    amount: Mapped[int]


class BuyStep(Base):
    __tablename__ = "buy_step"

    buy_step_id: Mapped[idpk]
    buy_id: Mapped[int] = mapped_column(
        ForeignKey("buy.buy_id", ondelete="CASCADE"), unique=True
    )
    buy: Mapped[Buy] = relationship(back_populates="buy_step", lazy="joined")
    step_id: Mapped[int] = mapped_column(
        ForeignKey("step.step_id", ondelete="CASCADE"), unique=True
    )
    step: Mapped[Step] = relationship(back_populates="buy_step", lazy="joined")
    date_step_beg: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()  # pylint: disable=E1102
    )
    date_step_end: Mapped[datetime.datetime]
