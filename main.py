from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from typing import List

# Create FastAPI instance
app = FastAPI()

# Define the PostgreSQL database URL
DATABASE_URL = "postgresql://arthur_191:pass123@localhost:5432/Pharmacy_Directory"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a base class for declarative models
Base = declarative_base()

# # Define the Medicine class as a SQLAlchemy model
class Medicine(Base):
    __tablename__ = "Medicine"

    # Define columns for the Medicine table
    quantity_per_package = Column(Integer, primary_key=True)
    manufacturer = Column(String(50))
    name = Column(String(50), unique=True)
    indications = Column(String(150))
    contraindications = Column(String(150))

# Define a Pydantic model for creating a new Medicine
class MedicineCreate(BaseModel):
    manufacturer: str
    name: str
    indications: str
    contraindications: str

# Define a Pydantic model for the Medicine response
class MedicineResponse(BaseModel):
    quantity_per_package: int
    manufacturer: str
    name: str
    indications: str
    contraindications: str

# Create the Medicine table in the database
Base.metadata.create_all(bind=engine)

# Create a SQLAlchemy session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a FastAPI dependency for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define FastAPI endpoint to create a new Medicine
@app.post("/medicines/", response_model=MedicineResponse)
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    # Create a new Medicine instance from the input data
    db_medicine = Medicine(**medicine.dict())

    # Add the new Medicine to the database session
    db.add(db_medicine)

    # Commit the changes to the database
    db.commit()

    # Refresh the Medicine instance to get updated values
    db.refresh(db_medicine)

    # Return the created Medicine as the response
    return db_medicine

# Define FastAPI endpoint to get all Medicines
@app.get("/medicines/", response_model=List[MedicineResponse])
def read_medicines(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Query the database to get a list of Medicines with pagination
    medicines = db.query(Medicine).offset(skip).limit(limit).all()

    # Return the list of Medicines as the response
    return medicines

# Define FastAPI endpoint to get a specific Medicine by quantity_per_package
@app.get("/medicines/{quantity_per_package}", response_model=MedicineResponse)
def read_medicine(quantity_per_package: int, db: Session = Depends(get_db)):
    # Query the database to get a specific Medicine by quantity_per_package
    medicine = db.query(Medicine).filter(Medicine.quantity_per_package == quantity_per_package).first()

    # If Medicine is not found, raise an HTTPException with status code 404
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")

    # Return the found Medicine as the response
    return medicine
