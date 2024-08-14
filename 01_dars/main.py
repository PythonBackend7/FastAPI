from fastapi import FastAPI

app = FastAPI(title='Just API', version='0.0.1', description='Just API')

fake_db = [{'Hello': "Mother and Father"}]


@app.get("/", description='get request')
async def root():
    return fake_db


@app.post('/create/')
async def create(item: dict):
    fake_db.append(item)
    return fake_db


@app.put('/update/')
async def update(item: dict):
    fake_db.append(item)
    return fake_db


@app.delete('/delete/')
async def delete(item: dict):
    fake_db.remove(item)
    return fake_db