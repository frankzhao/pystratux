import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from stratux.util import representable

Base = declarative_base()


@representable
class Traffic(Base):
    __tablename__ = 'traffic'

    id = Column(UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()'))
    icao_addr = Column(String)
    reg = Column(String)
    tail = Column(String)
    emitter_category = Column(Integer)
    onground = Column(Boolean)
    addr_type = Column(Integer)
    targettype = Column(Integer)
    signallevel = Column(Float)
    squawk = Column(Integer)
    position_valid = Column(Boolean)
    lat = Column(Float)
    lng = Column(Float)
    alt = Column(Integer)
    gnssdifffrombaroalt = Column(Boolean)
    altisgnss = Column(String)
    nic = Column(Integer)
    nacp = Column(Integer)
    track = Column(Integer)
    speed = Column(Integer)
    speed_valid = Column(Boolean)
    vvel = Column(Float)
    timestamp = Column(DateTime)
    prioritystatus = Column(Boolean)
    age = Column(Float)
    agelastalt = Column(Float)
    last_seen = Column(DateTime)
    last_alt = Column(DateTime)
    last_gnssdiff = Column(DateTime)
    last_gnssdiffalt = Column(Integer)
    last_speed = Column(DateTime)
    last_source = Column(Integer)
    extrapolatedposition = Column(Boolean)
    bearingdist_valid = Column(Boolean)
    bearing = Column(Integer)
    distance = Column(Integer)


