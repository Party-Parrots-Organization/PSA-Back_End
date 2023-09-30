import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://root:f42hoWXB0@localhost:3306/game')

# Create a base class for declarative models
Base = declarative_base()

# Define a model representing a Ship in the database
class Ship(Base):
    __tablename__ = 'ship'
    imo = Column(Integer, primary_key=True)
    ship_type = Column(Integer, primary_key=False)
    dim_a = Column(Integer, primary_key=False)
    dim_b = Column(Integer, primary_key=False)

class Port(Base):
    __tablename__ = 'port'
    port_code = Column(Integer, primary_key=True)
    lat = Column(Float, primary_key=False)
    lon = Column(Float, primary_key=False)
    port_name = Column(String, primary_key=False)

def get_all_ships():
    Session = sessionmaker(bind=engine)
    session = Session()
    ships = session.query(Ship).all()
    result = []

    # Print the retrieved data
    for ship in ships:
        ship_json = {
            "imo": ship.imo,
            "ship_type": ship.ship_type,
            "dim_a": ship.dim_a,
            "dim_b": ship.dim_b
        }
        result.append(ship_json)

    # Commit the transaction and close the session
    session.commit()
    session.close()
    return result

def get_all_ports():
    Session = sessionmaker(bind=engine)
    session = Session()
    ports = session.query(Port).all()
    result = []

    # Print the retrieved data
    for port in ports:
        port_json = {
            "port_code": port.port_code,
            "lat": port.lat,
            "lon": port.lon,
            "port_name": port.port_name
        }
        result.append(port_json)

    # Commit the transaction and close the session
    session.commit()
    session.close()
    return result

get_all_ships()