from sqlalchemy import Column, String

class Shortcut():
    __tablename__ = 'shortcuts'
    command = Column(String, primary_key=True)
    result = Column(String)