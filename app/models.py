from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    studios = Column(String, nullable=False)
    producers = Column(String, nullable=False)
    winner = Column(Boolean, nullable=True)
