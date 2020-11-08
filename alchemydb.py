# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

Base = declarative_base()
RDB_PATH = 'postgresql+psycopg2://rsuser:rsuser_password@db:5432/responder'
#RDB_PATH = 'sqlite:///db.sqlite3'
ECHO_LOG = False
engine = create_engine(
   RDB_PATH, echo=ECHO_LOG, pool_size=20, max_overflow=0
   #RDB_PATH, echo=ECHO_LOG
)
Session = sessionmaker(bind=engine)
session = Session()