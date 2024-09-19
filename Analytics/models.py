from sqlalchemy import BigInteger, Column, ForeignKey, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'

    movieId = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String)
    genres = Column(String)

class Rating(Base):
    __tablename__ = 'ratings'

    ratingid = Column(Integer, primary_key = True, autoincrement = True)
    userid = Column(Integer)
    movieid = Column(Integer, ForeignKey('movies.movieid'))
    rating = Column(Float)
    timestamp = Column(BigInteger)