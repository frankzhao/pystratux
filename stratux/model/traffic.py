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
    gnssdifffrombaroalt = Column(Integer)
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

    def __init__(self, id=None, icao_addr=None, reg=None, tail=None, emitter_category=None, onground=None,
                 addr_type=None, targettype=None, signallevel=None, squawk=None, position_valid=None, lat=None,
                 lng=None, alt=None, gnssdifffrombaroalt=None, altisgnss=None, nic=None, nacp=None, track=None,
                 speed=None, speed_valid=None, vvel=None, timestamp=None, prioritystatus=None, age=None,
                 agelastalt=None, last_seen=None, last_alt=None, last_gnssdiff=None, last_gnssdiffalt=None,
                 last_speed=None, last_source=None, extrapolatedposition=None, bearingdist_valid=None,
                 bearing=None, distance=None):
        self.id = id
        self.icao_addr = icao_addr
        self.reg = reg
        self.tail = tail
        self.emitter_category = emitter_category
        self.onground = onground
        self.addr_type = addr_type
        self.targettype = targettype
        self.signallevel = signallevel
        self.squawk = squawk
        self.position_valid = position_valid
        self.lat = lat
        self.lng = lng
        self.alt = alt
        self.gnssdifffrombaroalt = gnssdifffrombaroalt
        self.altisgnss = altisgnss
        self.nic = nic
        self.nacp = nacp
        self.track = track
        self.speed = speed
        self.speed_valid = speed_valid
        self.vvel = vvel
        self.timestamp = timestamp
        self.prioritystatus = prioritystatus
        self.age = age
        self.agelastalt = agelastalt
        self.last_seen = last_seen
        self.last_alt = last_alt
        self.last_gnssdiff = last_gnssdiff
        self.last_gnssdiffalt = last_gnssdiffalt
        self.last_speed = last_speed
        self.last_source = last_source
        self.extrapolatedposition = extrapolatedposition
        self.bearingdist_valid = bearingdist_valid
        self.bearing = bearing
        self.distance = distance
