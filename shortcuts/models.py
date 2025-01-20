from sqlalchemy import Column, String
from database import Base

class Shortcut(Base):
    __tablename__ = 'shortcuts'
    command = Column(String, primary_key=True)
    result = Column(String)