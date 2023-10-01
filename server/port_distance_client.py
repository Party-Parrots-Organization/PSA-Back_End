import os
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://root:f42hoWXB0@localhost:3306/game')

# Create a base class for declarative models
Base = declarative_base()

class Port_Distance(Base):
    __tablename__ = 'port_distance'
    port_1_name = Column(String, primary_key=True)
    port_2_name = Column(String, primary_key=True)
    route_distance = Column(Float, primary_key=False)

def get_route_distance(port_1_name, port_2_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    route_dist = session.query(Port_Distance).filter_by(port_1_name=port_1_name).filter_by(port_2_name=port_2_name).first()
    result = route_dist.route_distance
    # Close the session
    session.close()
    return result

print(get_route_distance("GUAM", "ZHOUSHAN"))