from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title='Mini Project')


class Car(BaseModel):
    name: str
    price: Optional[float]
    color: str
    speed: int
    description: Optional[str] = None


all_cars = [
    {'id': 1,
     'name': 'BMW m5',
     'price': 540000.50,
     'color': 'blue',
     'speed': 520,
     'description': 'BMW M5 competition'},
]

@app.get("/cars/")
def get_cars():
    return all_cars

@app.post("/cars/")
def create_car(car: Car):
    data = Car(**car.dict())
    data.name = car.name
    data.price = car.price
    data.color = car.color
    data.speed = car.speed
    data.description = car.description
    data.save()
    return {'status_code': 201, 'data': data}

@app.get("/cars/{id}")
def get_car(id: int):
    return all_cars[id-1]
