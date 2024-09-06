import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from tortoise.contrib.fastapi import register_tortoise
import models, schemas
from typing import List


app = FastAPI(title='CRUD API')

@app.post('/items/', response_model=schemas.ItemRead)
async def create_item(item: schemas.ItemRead):
    obj = await models.Item.create(**item.dict())
    return obj

@app.get('/items/', response_model=List[schemas.ItemRead])
async def read_items():
    objs = await models.Item.all()
    # objs = await models.Item.all()
    return objs

@app.get('/items/{item_id}/', response_model=schemas.ItemRead)
async def read_item(item_id: int):
    obj = await models.Item.get(id=item_id)
    # obj = await models.Item.get_or_none(item_id=item_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return obj

@app.put('/items/{item_id}', response_model=schemas.ItemRead)
async def update_item(item_id: int, item: schemas.ItemRead):
    obj = await models.Item.get_or_none(id=item_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Item not found')
    data = item.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(obj, key, value)
    await obj.save()
    return obj


@app.delete('/items/{item_id}/', response_model=schemas.ItemRead)
async def delete_item(item_id: int):
    obj = await models.Item.get(id=item_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Item not found')
    await obj.delete()
    return {'message': f'Item deleted successfully'}


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
