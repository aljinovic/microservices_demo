from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///../db.sqlite', echo=False)
Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    surname = Column(String(100), nullable=True)
    email = Column(String(200), nullable=True, unique=True)
    phone = Column(String(20), nullable=True, unique=False)

    def __repr__(self):
        return '<Contacts %r>' % self.name


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()
