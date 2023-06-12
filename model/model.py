from sqlalchemy import Column, ForeignKey, Integer, String, VARCHAR, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CPU(Base):
    __table__ = 'processor'

    code = Column(Integer, primary_key=True)
    display_name = Column(VARCHAR(200))
    brand = Column(String(50))
    socket = Column(String(50))
    image = Column(VARCHAR(200))
    price = Column(Integer)

class Monitor(Base):
    __table__ = 'monitor'

    code = Column(Integer, primary_key=True)
    display_name = Column(VARCHAR(200))
    image = Column(VARCHAR(200))
    price = Column(Integer)

class GPU(Base):
    __table__ = 'gpu'

    code = Column(Integer, primary_key=True)
    display_name = Column(VARCHAR(200))
    brand = Column(String(50))
    size = Column(VARCHAR(10))
    image = Column(VARCHAR(200))
    price = Column(Integer)

class RAM(Base):
    __table__ = 'ram'

    code = Column(Integer, primary_key=True)
    display_name = Column(VARCHAR(200))
    size = Column(VARCHAR(10))
    ram_type = Column(VARCHAR(10))
    image = Column(VARCHAR(200))
    price = Column(Integer)

class StorageHDD(Base):
    __table__ = 'hdd'

    code = Column(Integer, primary_key=True)
    display_name = Column(VARCHAR(200))
    size = Column(VARCHAR(10))
    image = Column(VARCHAR(200))
    price = Column(Integer)

class StorageSSD(Base):
    __table__ = 'ssd'

    code = Column(Integer, primary_key=True)
    display_name = Column(VARCHAR(200))
    size = Column(VARCHAR(10))
    image = Column(VARCHAR(200))
    price = Column(Integer)