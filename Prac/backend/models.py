from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(255), index = True)
    option = relationship("Option", back_populates = "category")

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(255), index = True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates = "option")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key = True)
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key = True)
    option_id = Column(Integer, ForeignKey("options.id"))


