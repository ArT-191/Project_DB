from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.sql.expression import Index


Base = declarative_base()

class Medicine(Base):
    __tablename__ = "Medicine"

    quantity_per_package = Column(Integer, primary_key=True)
    manufacturer = Column(String(50))
    name = Column(String(50), unique=True)
    indications = Column(String(150))
    contraindications = Column(String(150))
    description = Column(String(200))
    extra_data = Column(JSONB)

    # One-to-Many relationship with Availability
    availabilities = relationship('Availability', back_populates='medicine', cascade="all, delete-orphan")


Index('idx_medicine_extra_data_gin', Medicine.extra_data, postgresql_using='gin')


class Availability(Base):
    __tablename__ = "Availability"

    price = Column(Numeric(precision=10, scale=2), primary_key=True)
    date = Column(String(25))
    count = Column(Integer, CheckConstraint('count > 0'))
    expiration_date = Column(String(25))
    extra_data = Column(JSONB)

    # Many-to-One relationship with Medicine
    medicine_quantity_per_package = Column(Integer, ForeignKey('Medicine.quantity_per_package'))
    medicine = relationship('Medicine', back_populates='availabilities')

    # Many-to-One relationship with Pharmacy
    pharmacy_name = Column(String(30), ForeignKey('Pharmacy.pharmacy_name'))
    pharmacy = relationship('Pharmacy', back_populates='availabilities')

class Pharmacy(Base):
    __tablename__ = "Pharmacy"

    telephone = Column(String(25))
    address = Column(String(100))
    pharmacy_name = Column(String(30), primary_key=True)
    specialization = Column(String(30))
    working_time = Column(String(30))
    extra_data = Column(JSONB)

    # One-to-Many relationship with Availability
    availabilities = relationship('Availability', back_populates='pharmacy', cascade="all, delete-orphan")

DATABASE_URL = "postgresql://arthur_191:pass123@localhost:5432/Pharmacy_Directory"
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
