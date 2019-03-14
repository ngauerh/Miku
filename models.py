from settings import DB
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Sequence
from sqlalchemy import func
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?charset=utf8'.format(
    USERNAME=DB['USER'],
    PASSWORD=DB['PASSWORD'],
    HOST=DB['HOST'],
    PORT=DB['PORT'],
    DB_NAME=DB['DB_NAME'],
), convert_unicode=True, echo=False)


DBSession = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = DBSession.query_property()

Base = declarative_base()


def init_db(db_engine):
    Base.metadata.create_all(bind=db_engine)
    # Base.metadata.tables["proxy"].create(bind=db_engine)


class Proxy(Base):
    __tablename__ = 'proxy'
    id = Column(Integer, Sequence('proxy_id_seq'), primary_key=True)
    ip = Column(String(255), unique=True)
    port = Column(String(255))
    code = Column(String(255))
    country = Column(String(255))
    anonymity = Column(String(250))
    https = Column(String(255))
    create_at = Column(DateTime(timezone=True), default=func.now())


if __name__ == '__main__':
    init_db(engine)
