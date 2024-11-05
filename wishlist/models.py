from wishlist.database.db import Base, engine
from sqlalchemy import Column, String, Integer, Boolean


class Item(Base):
    __tablename__ = 'wishlist'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Integer)
    is_complete = Column(Boolean, default=False)


# Base.metadata.create_all(bind=engine)