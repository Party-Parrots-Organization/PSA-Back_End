import os
import json
import geohash_tools as gh
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv('DB_URL')
engine = create_engine(db_url)

# Create a base class for declarative models
Base = declarative_base()

class Port(Base):
    __tablename__ = 'port'
    port_code = Column(Integer, primary_key=True)
    lat = Column(Float, primary_key=False)
    lon = Column(Float, primary_key=False)
    port_name = Column(String, primary_key=False)
    geohash = Column(Integer, primary_key=False)

def get_all_ports():
    Session = sessionmaker(bind=engine)
    session = Session()
    ports = session.query(Port).all()
    result = json.dumps([{"port_code": port.port_code, "lat": port.lat, "lon": port.lon, "port_name": port.port_name} for port in ports])
    # Close the session
    session.close()
    return result

def get_port_code(port_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    port_code = session.query(Port).filter_by(port_name=port_name).first().port_code
    result = port_code
    # Close the session
    session.close()
    return result

def get_port_geohash(port_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Port).filter_by(port_name=port_name).first().geohash
    # Close the session
    session.close()
    return result

def get_port_coordinates(port_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Port).filter_by(port_name=port_name).first()
    # Close the session
    session.close()
    return result.lat, result.lon

# print(get_all_ports())