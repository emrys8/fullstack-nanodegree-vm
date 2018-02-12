import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(Integer, nullable=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class MenuItem(Base):
    __tablename__ = 'menu_item'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    course = Column(String(200))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        # Returns the instance data in an easily serializable format
        return {
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'id': self.id,
            'course': self.course
        }



engine = create_engine('sqlite:///restaurant_menu.db')
Base.metadata.create_all(engine)

