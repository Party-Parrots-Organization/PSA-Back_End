import os
import json
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
    name = Column(String, primary_key=False)

def get_all_ships():
    Session = sessionmaker(bind=engine)
    session = Session()
    ships = session.query(Ship).all()
    result = json.dumps([{"imo": ship.imo, "ship_type": ship.ship_type, "dim_a": ship.dim_a, "dim_b": ship.dim_b, "ship_name": ship.name} for ship in ships])

    # Commit the transaction and close the session
    session.close()
    return result

def get_ship_by_imo(imo):
    Session = sessionmaker(bind=engine)
    session = Session()
    ship = session.query(Ship).filter_by(imo = imo).first()
    return json.dumps({
        "imo": ship.imo,
        "ship_type": ship.ship_type,
        "dim_a": ship.dim_a,
        "dim_b": ship.dim_b,
        "ship_name": ship.name
    })

ship = json.loads(get_ship_by_imo(0))
print(get_all_ships())
print(ship.get("ship_type"))