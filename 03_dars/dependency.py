from urllib.request import Request

from fastapi import FastAPI, Depends, HTTPException

app = FastAPI(title='Routing and path operation')





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