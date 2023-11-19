from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, ForeignKey, CheckConstraint, func, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()

class Medicine(Base):
    __tablename__ = "Medicine"

    quantity_per_package = Column(Integer, primary_key=True)
    manufacturer = Column(String(50))
    name = Column(String(50), unique=True)
    indications = Column(String(150))
    contraindications = Column(String(150))
    description = Column(String(200))  # New field

    # One-to-Many relationship with Availability
    availabilities = relationship('Availability', back_populates='medicine')

class Availability(Base):
    __tablename__ = "Availability"

    price = Column(Numeric(precision=10, scale=2), primary_key=True)
    date = Column(DateTime, default=func.now())
    count = Column(Integer, CheckConstraint('count > 0'))
    expiration_date = Column(DateTime)

    
    # Many-to-One relationship with Pharmacy
    pharmacy_name = Column(String(30), ForeignKey('Pharmacy.pharmacy_name'))
    pharmacy = relationship('Pharmacy', back_populates='availabilities')

class Pharmacy(Base):
    __tablename__ = "Pharmacy"

    telephone = Column(String(25))
    address = Column(String(100))
    pharmacy_name = Column(String(30), primary_key=True)
    specialization = Column(String(30))

DATABASE_URL = "postgresql://arthur_191:pass123@localhost:5432/Pharmacy_Directory"
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
