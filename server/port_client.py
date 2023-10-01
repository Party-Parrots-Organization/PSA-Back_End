import os
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://root:f42hoWXB0@localhost:3306/game')

# Create a base class for declarative models
Base = declarative_base()

class Port(Base):
    __tablename__ = 'port'
    port_code = Column(Integer, primary_key=True)
    lat = Column(Float, primary_key=False)
    lon = Column(Float, primary_key=False)
    port_name = Column(String, primary_key=False)

def get_all_ports():
    Session = sessionmaker(bind=engine)
    session = Session()
    ports = session.query(Port).all()
    result = json.dumps([{"port_code": port.port_code, "lat": port.lat, "lon": port.lon, "port_name": port.port_name} for port in ports])
    # Commit the transaction and close the session
    session.commit()
    session.close()
    return result

print(get_all_ports())