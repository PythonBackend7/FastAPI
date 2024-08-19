from urllib.request import Request

from fastapi import FastAPI, Depends, HTTPException

app = FastAPI(title='Routing and path operation')


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/{user_id}")
async def users(user_id: int):
    return {'user_id': user_id}


# Get /users/12  user_id = 12

@app.get('/items')
async def items(skip: int = 0, limit: int = 10):
    return {'skip': skip, 'limit': limit}


# GET /items/?skip=2&limit=9

@app.get('/products/{product_type}/{product_id}')
async def products(product_type: str, product_id: int):
    return {'product_type': product_type, 'product_id': product_id}


# GET /products/laptop/12   {'product_type': 'laptop', 'product_id': 12}

# GET
@app.get('/items/{id}')
async def items(id: int):
    return {'id': id}


# POST
@app.post('/items/')
async def items_create(name: str, description: str, price: float):
    return {'name': name, 'description': description, 'price': price}


@app.put('/items/{id}')
async def items_update(id: int, name: str, description: str, price: float):
    return {'id': id, 'name': name, 'description': description, 'price': price}


@app.delete('/items/{id}')
async def items_delete(id: int):
    return {'message': 'Item deleted'}


def common_dependency():
    return {'message': 'Common dependencies'}


@app.get('/items/')
def read_items(common: dict = Depends(common_dependency)):
    return {'common': common}


def query_params(skip: int = 0, limit: int = 10):
    return {'skip': skip, 'limit': limit}

def user_authentication(token: str):
    if token != 'superusertoken':
        raise HTTPException(status_code=400, detail='Invalid token')
    return {'user': 'authenticated'}


@app.get('/items')
def read_items(common: dict = Depends(common_dependency), query_params: dict = Depends(query_params), user_authentication=Depends(user_authentication)):
    return {'common': common, 'query_params': query_params, 'user_authentication': user_authentication}


@app.middleware('http')
async def global_dependency(request: Request, call_next):
    response = await call_next(request)
    response.headers['X-Global-Dependency'] = 'Bu Global Dependency'
    return response


@app.get('/users/')
def read_user(user: dict = Depends(user_authentication)):
    return {'user': user}
