from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()

class Weather(Base):
    __tablename__ = 'weather'
    
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    hour = Column(Integer)
    minute  = Column(Integer)
    temp_out = Column(Float)
    temp_in = Column(Float)
    humidity_out = Column(Integer)
    humidity_in = Column(Float)
    wind_v = Column(Float)
    wind_d = Column(Float)
    pressure_in = Column(Float)
    rain = Column(Float)
    
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def write_db(weather_data):
    session = Session()
    session.add(Weather(**weather_data))
    session.commit()
    for instance in session.query(Weather).order_by(Weather.id):
        print(instance.temp_out)
        print(instance.rain)
        print(instance.humidity_out)
