from sqlalchemy import Column, ForeignKey, Integer, String, VARCHAR, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CPU(Base):
    __table__ = 'cpu'

    PCODE = Column(Integer, primary_key=True)
    PNAME = Column(VARCHAR(200))
    PPRCZ0 = Column(Integer)
    PPRCZ1 = Column(Integer)

class Monitor(Base):
    __table__ = 'prosesor'

    PCODE = Column(Integer, primary_key=True)
    PNAME = Column(VARCHAR(200))
    PPRCZ0 = Column(Integer)
    PPRCZ1 = Column(Integer)

class GPU(Base):
    __table__ = 'gpu'

    PCODE = Column(Integer, primary_key=True)
    PNAME = Column(VARCHAR(200))
    PPRCZ0 = Column(Integer)
    PPRCZ1 = Column(Integer)

class RAM(Base):
    __table__ = 'ram'

    PCODE = Column(Integer, primary_key=True)
    PNAME = Column(VARCHAR(200))
    PPRCZ0 = Column(Integer)
    PPRCZ1 = Column(Integer)

class StorageHDD(Base):
    __table__ = 'hdd'

    PCODE = Column(Integer, primary_key=True)
    PNAME = Column(VARCHAR(200))
    PPRCZ0 = Column(Integer)
    PPRCZ1 = Column(Integer)

class StorageSSD(Base):
    __table__ = 'ssd'

    PCODE = Column(Integer, primary_key=True)
    PNAME = Column(VARCHAR(200))
    PPRCZ0 = Column(Integer)
    PPRCZ1 = Column(Integer)