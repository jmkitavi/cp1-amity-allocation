import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Employees(Base):
    __tablename__ = "employees"
    emp_name = Column(String(32), primary_key=True, nullable=False)
    emp_role = Column(String(32), nullable=False)


class Rooms(Base):
    __tablename__ = "rooms"

    room_name = Column(String(32), primary_key=True, nullable=False)
    room_type = Column(String(32), nullable=False)


class Allocations(Base):
    __tablename__ = "allocations"
    __table_args__ = {'extend_existing': True}
    room_name = Column(String(32), primary_key=True, nullable=False)
    room_type = Column(String(32), nullable=False)
    occupants = Column(String(250))


class Unallocated(Base):
    __tablename__ = "unallocated"
    room_type = Column(String(32), primary_key=True, nullable=False)
    unallocated = Column(String(250))


class DatabaseCreator(object):
    def __init__(self, db_name):
        self.db_name = db_name + '.sqlite'
        self.engine = create_engine('sqlite:///' + self.db_name)
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(self.engine)
