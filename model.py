from sqlalchemy import Column, DateTime, String, Float, Integer, ForeignKey
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from private import engine

Base = declarative_base()

class City(Base):
    __tablename__ = 'city'
    id   = Column(Integer, primary_key=True)
    name = Column(String)

class Measurement(Base):
    __tablename__ = 'measurement'
    id      = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id'))
    city    = relationship(City, backref=backref('measuments', uselist=True))
    stamp   = Column(DateTime)
    value   = Column(Float)
    unit    = Column(String)

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

def measurement(city_name, value, unit):
    s = session()
    measurement = Measurement(value=value, unit=unit, stamp=datetime.now())
    measurement.city = s.query(City).filter(City.name == city_name).one()
    s.add(measurement)
    s.commit()

def measurements(city_name):
    s = session()
    city = s.query(City).filter(City.name == city_name).one()
    return s.query(Measurement).filter(Measurement.city_id == city.id)

def city(city_name):
    s = session()
    s.add(City(name=city_name))
    s.commit()
