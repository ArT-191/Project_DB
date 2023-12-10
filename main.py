from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional


# Use your existing SQLAlchemy models
from models import Medicine, Availability, Pharmacy

DATABASE_URL = "postgresql://arthur_191:pass123@localhost:5432/Pharmacy_Directory"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()

# Create Pydantic models for request and response
class MedicineCreate(BaseModel):
    quantity_per_package: int
    manufacturer: str
    name: str
    indications: str
    contraindications: str


class MedicineResponse(MedicineCreate):
    pass

class AvailabilityCreate(BaseModel):
    price: float
    date: str
    count: int
    expiration_date: str

class AvailabilityResponse(AvailabilityCreate):
    date: str

class PharmacyCreate(BaseModel):
    telephone: str
    address: str
    pharmacy_name: str
    specialization: str
    working_time: str

class PharmacyResponse(PharmacyCreate):
    pass

# Create FastAPI app
app = FastAPI(debug=True)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations for Medicine
@app.post("/medicines/", response_model=MedicineResponse)
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    try:
        db_medicine = Medicine(**medicine.dict())
        db.add(db_medicine)
        db.commit()
        db.refresh(db_medicine)
        return db_medicine
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/medicines/{medicine_name}", response_model=MedicineResponse)
def read_medicine(medicine_name: str, db: Session = Depends(get_db)):
    medicine = db.query(Medicine).filter(Medicine.name == medicine_name).first()
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@app.get("/medicines/", response_model=List[MedicineResponse])
def list_medicines(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    medicines = db.query(Medicine).offset(skip).limit(limit).all()
    return medicines

# CRUD operations for Availability
@app.post("/availabilities/", response_model=AvailabilityResponse)
def create_availability(availability: AvailabilityCreate, db: Session = Depends(get_db)):
    db_availability = Availability(**availability.dict())
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability

@app.get("/availabilities/{price}", response_model=AvailabilityResponse)
def read_availability(price: float, db: Session = Depends(get_db)):
    availability = db.query(Availability).filter(Availability.price == price).first()
    if availability is None:
        raise HTTPException(status_code=404, detail="Availability not found")
    return availability

@app.get("/availabilities/", response_model=List[AvailabilityResponse])
def list_availabilities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    availabilities = db.query(Availability).offset(skip).limit(limit).all()
    return availabilities

# CRUD operations for Pharmacy
@app.post("/pharmacies/", response_model=PharmacyResponse)
def create_pharmacy(pharmacy: PharmacyCreate, db: Session = Depends(get_db)):
    db_pharmacy = Pharmacy(**pharmacy.dict())
    db.add(db_pharmacy)
    db.commit()
    db.refresh(db_pharmacy)
    return db_pharmacy

@app.get("/pharmacies/{pharmacy_name}", response_model=PharmacyResponse)
def read_pharmacy(pharmacy_name: str, db: Session = Depends(get_db)):
    pharmacy = db.query(Pharmacy).filter(Pharmacy.pharmacy_name == pharmacy_name).first()
    if pharmacy is None:
        raise HTTPException(status_code=404, detail="Pharmacy not found")
    return pharmacy

# 1. SELECT ... WHERE (с несколькими условиями)
@app.get("/medicines/filter/", response_model=List[MedicineResponse])
def filter_medicines(manufacturer: str, indications: str, db: Session = Depends(get_db)):
    medicines = db.query(Medicine).filter(
        Medicine.manufacturer == manufacturer,
        Medicine.indications == indications
    ).all()
    return medicines

# 2. JOIN
@app.get("/medicines/{medicine_id}/availability/", response_model=List[AvailabilityResponse])
def get_medicine_availability(medicine_id: int, db: Session = Depends(get_db)):
    medicine_availability = db.query(Availability).join(Medicine).filter(Medicine.id == medicine_id).all()
    return medicine_availability

# 3. UPDATE с нетривиальным условием
@app.put("/update-availability/", response_model=AvailabilityResponse)
def update_availability_price_threshold(price_threshold: float, new_count: int, db: Session = Depends(get_db)):
    updated_availability = db.query(Availability).filter(Availability.price > price_threshold).update(
        {Availability.count: new_count}, synchronize_session=False)
    db.commit()
    return updated_availability

# 4. GROUP BY
@app.get("/availability-by-manufacturer/", response_model=List[dict])
def availability_by_manufacturer(db: Session = Depends(get_db)):
    result = db.query(Medicine.manufacturer, func.sum(Availability.count)).join(Availability).group_by(
        Medicine.manufacturer).all()
    return [{"manufacturer": m, "total_count": count} for m, count in result]

# 5. Добавить сортировку выдачи результатов по какому-то из полей
@app.get("/pharmacies/", response_model=List[PharmacyResponse])
def list_pharmacies_sorted(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pharmacies = db.query(Pharmacy).order_by(Pharmacy.pharmacy_name).offset(skip).limit(limit).all()
    return pharmacies
