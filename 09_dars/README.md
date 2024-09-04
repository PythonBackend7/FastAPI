# FastAPI and Tortoise ORM
FastAPI bilan Tortoise-ORM ishlatish – ma'lumotlar bazasiga ulanish va CRUD operatsiyalarini bajarish uchun qulay yondashuvlardan biridir. Tortoise-ORM - bu Pythonda yozilgan engil ORM bo'lib, asinxron dasturlar uchun maxsus mo'ljallangan. Ushbu darsda FastAPI bilan Tortoise-ORMni qanday sozlash va ishlatishni ko'rib chiqamiz.
1. Muhitni sozlash
Birinchi navbatda, kerakli kutubxonalarni o'rnatamiz:
```shell
pip install fastapi uvicorn
pip install passlib
pip install bcrypt
pip install pydantic[email]
pip install email-validator
pip install aerich
```
2. Aerich ni Tortoise bilan o'rnatish va konfiguratsiya qilish:
Aerich, Tortoise ORM uchun migratsiya vositasi hisoblanadi. Quyidagi amallarni bajaring:

aerich init ni bajaring: Bu buyruq aerich.ini konfiguratsiya faylini yaratadi va ma'lumotlar bazasidagi migratsiyalarni boshqarish uchun migrations papkasini yaratadi.
```shell
aerich init -t config.TORTOISE_ORM
```
Bu erda -t config.TORTOISE_ORM bu sizning Tortoise ORM konfiguratsiyangizni qaerdan olish kerakligini bildiradi (config.py faylidan)
* aerich init-db ni bajaring: Bu buyruq dastlabki ma'lumotlar bazasini yaratish uchun ishlatiladi va dastlabki migratsiyalarni yaratadi.
```shell
aerich init-db
```

4. Migrations yaratish va ulash:
Yangi migratsiyalarni yaratish uchun: Agar siz yangi model yoki o'zgartirish qo'shsangiz, quyidagi buyruqni bajaring:
```shell
aerich migrate
```
5. Mavjud migratsiyalarni ulash uchun:
```shell
aerich upgrade
```

6. Xulosa:
Bu qadamlarni bajarganingizdan so'ng, aerich.models moduli topilmasligi bilan bog'liq xato bartaraf etiladi. Aerich migratsiya jarayonlarini boshqarish uchun foydalanadi va ushbu modullarni ma'lumotlar bazasini yangilash yoki qayta yaratishda ishlatadi.


* fastapi: Asosiy API ramkasi.
* tortoise-orm[asyncpg]: Tortoise ORM va asyncpg - PostgreSQL bilan ishlash uchun.
* uvicorn: Asgi server.

2. Loyihaning tuzilishi
Loyihani quyidagi tarzda tuzamiz:
```css
my_fastapi_project
├── main.py
├── models.py
├── schemas.py
├── config.py

```

* main.py: Asosiy ilova fayli.
* models.py: Tortoise ORM modellari.
* schemas.py: Pydantic sxemalari.
* config.py: Tortoise ORM sozlamalari.

3. Tortoise-ORM konfiguratsiyasi (config.py)
```shell
TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3"  # SQLite ma'lumotlar bazasiga ulanish satri
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # `models` - bizning modellari, `aerich.models` - Tortoise migrations uchun
            "default_connection": "default",
        }
    },
}
```

### Bu yerda:

* sqlite://db.sqlite3: Bu SQLite ulanish satri bo'lib, db.sqlite3 fayl nomini bildiradi. Agar bu fayl mavjud bo'lmasa, Tortoise uni avtomatik ravishda yaratadi.
* connections va apps bo'limlari Tortoise ORM uchun ulanish va ilova sozlamalarini belgilaydi.

4. Ma'lumotlar bazasi modellari (models.py)
```shell
# models.py

from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)

    def __str__(self):
        return self.email
```

### Bu yerda:

* User modeli users jadvaliga mos keladi.
* fields yordamida ma'lumotlar turini va xususiyatlarini belgilaymiz.

5. Pydantic sxemalari (schemas.py)
```shell
# schemas.py

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

```
* UserBase: foydalanuvchi asosiy ma'lumotlari uchun Pydantic model.
* UserCreate: foydalanuvchi yaratish uchun model.
* User: foydalanuvchini o'qish uchun model.

6. Asosiy ilova (main.py)
```shell
# main.py

from fastapi import FastAPI, HTTPException, Depends
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.context import CryptContext

import models
import schemas
from config import TORTOISE_ORM

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
User_Pydantic = pydantic_model_creator(models.User, name="User")
UserIn_Pydantic = pydantic_model_creator(models.User, name="UserIn", exclude_readonly=True)

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate):
    user_obj = models.User(email=user.email, hashed_password=pwd_context.hash(user.password))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@app.get("/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int):
    user = await models.User.filter(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await User_Pydantic.from_tortoise_orm(user)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

```

7. Tushuntirish:
* register_tortoise: Tortoise ORM-ni FastAPI bilan birlashtiradi.
* pydantic_model_creator: Tortoise modellari asosida Pydantic sxemalarini yaratadi.
* create_user: Yangi foydalanuvchini yaratish uchun POST /users/ endpointi.
* get_user: Foydalanuvchini olish uchun GET /users/{user_id} endpointi.

8. Ilovani ishga tushirish
Ilovani quyidagi buyruq orqali ishga tushirish mumkin:
```shell
uvicorn main:app --reload
```
Bu bilan sizda Tortoise-ORM bilan ishlaydigan FastAPI ilovasi bo'ladi. Bu ilovada foydalanuvchilarni yaratish va ma'lumotlarini olish imkoniyatlari mavjud.
