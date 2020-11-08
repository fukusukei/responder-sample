# -*- coding: utf-8 -*-
import os
from alchemydb import Base, engine
from sqlalchemy import Column, Integer, String, Text, text, DateTime
from datetime import datetime

class User(Base):
    dt_now = datetime.now()
    print(dt_now)
    
    __tablename__ = "users"
    id = Column('id', Integer, primary_key = True)
    username = Column('username', String(32))
    mailaddress = Column('mailaddress', String(255))
    password = Column('password', String(255))
    role = Column('role', String(255))
    created_at = Column('created_at', DateTime, nullable=False, default=dt_now)
    updated_at = Column('updated_at', DateTime, nullable=False, default=dt_now, onupdate=dt_now)

if __name__ == "__main__":
    Base.metadata.create_all(engine)