from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='Product API')

class Product(BaseModel):
    name: str
    price: int
    description: str = None
    image: str = None

products = []


@app.get("/")
def read_root():
    return products


@app.post('/product/')
def create_product(product: Product):
    products.append(product)
    return {'message': 'data created successfully'}

@app.get('/product/{id}')
def read_product(id: int):
    return products.pop(id-1)