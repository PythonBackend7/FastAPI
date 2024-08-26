from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from typing import List
import models
import schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='resume API', description='API for resume')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/about/', response_model=schemas.About)
async def create_about(data: schemas.AboutCreate, db: Session = Depends(get_db)):
    info = models.About(**data.dict())
    db.add(info)
    db.commit()
    db.refresh(info)
    return info

@app.get('/about-get/', response_model=List[schemas.About])
async def get_about(db: Session = Depends(get_db)):
    return db.query(models.About).all()

@app.post('/experience/', response_model=schemas.Experience)
async def create_experience(experience: schemas.ExperienceCreate, db: Session = Depends(get_db)):
    exp = models.Experience(**experience.dict())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

@app.get('/experience-get/', response_model=List[schemas.Experience])
async def get_experience(db: Session = Depends(get_db)):
    return db.query(models.Experience).all()


@app.post('/education/', response_model=schemas.Education)
async def create_education(edu: schemas.EducationCreate, db: Session = Depends(get_db)):
    exp = models.Education(**edu.dict())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

@app.get('/education-get/', response_model=List[schemas.Education])
async def education_get(db: Session = Depends(get_db)):
    return db.query(models.Education).all()

