import sys, os

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Employee(Base):

    __tablename__ = 'employee'

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)


class Address(Base):

    __tablename__ = 'address'

    id = Column(Integer, primary_key = True)

    Street = Column(String(80))
    Zip = Column(String(5))

    employee_id = Column(Integer, ForeignKey('employee.id'))

    employee = relationship(Employee)


# create engine
engine = create_engine('sqlite:///employee.db')

Base.metadata.create_all(engine)