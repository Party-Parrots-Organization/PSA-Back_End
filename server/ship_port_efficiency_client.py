import os
import json
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

class Ship_Port_Efficiency(Base):
    __tablename__ = 'ship_port_efficiency'
    imo = Column(Integer, primary_key=True)
    port_name = Column(String, primary_key=True)
    efficiency = Column(Float, primary_key=False)

def get_efficiency(ship_imo, port_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    route_dist = session.query(Ship_Port_Efficiency).filter_by(imo=ship_imo).filter_by(port_name=port_name).first()
    result = route_dist.efficiency
    # Close the session
    session.close()
    return result

print(get_efficiency(0, "GUAM"))