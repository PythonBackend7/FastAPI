# Tortoise-ORM ToDo CRUD
FastAPI yordamida Tortoise ORM orqali CRUD (Create, Read, Update, Delete) amallarini yozamiz va har bir kod bo'lagini tushuntirib o'taman. CRUD operatsiyalari asosan ma'lumotlar bazasidagi obyektlarni yaratish (Create), o'qish (Read), yangilash (Update) va o'chirish (Delete) uchun ishlatiladi.
### Loyihani quyidagi katalog tuzilmasida tashkil qilamiz:
```shell

├── project
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
└── db.sqlite3

```

### Paketlarni o'rnatish
Birinchi navbatda kerakli paketlarni o'rnatamiz:
```shell
pip install fastapi tortoise-orm aerich python-multipart uvicorn
```
1. config.py fayli
Bu faylda ma'lumotlar bazasini sozlaymiz. Biz SQLite ma'lumotlar bazasidan foydalanamiz:
```shell
# app/config.py

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},  # SQLite ma'lumotlar bazasi URI
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # Bizning modellar va migratsiya uchun kerakli modul
            "default_connection": "default",
        }
    },
}

```

2. models.py fayli
Ma'lumotlar bazasi modellari Tortoise ORM yordamida aniqlanadi. Bunda biz Item modelini yaratamiz, bu model CRUD amallarida ishlatiladi.
```shell
# app/models.py

from tortoise import fields, models

class Item(models.Model):
    id = fields.IntField(pk=True)  # Birlamchi kalit (Primary Key)
    name = fields.CharField(max_length=255)  # Nomi
    description = fields.TextField(null=True, blank=True)  # Ta'rifi
    price = fields.DecimalField(max_digits=10, decimal_places=2)  # Narxi
    created_at = fields.DatetimeField(auto_now_add=True)  # Yaratilgan vaqti
    updated_at = fields.DatetimeField(auto_now=True)  # Yangilangan vaqti

```
Tushuntirish:

* Item modeli bu ma'lumotlar bazasidagi obyekt (jadval) bo'lib, uning har bir ustuni uchun turli xil maydonlar (fields) mavjud.
* id — bu primary key (birlamchi kalit) bo'lib, avtomatik tarzda yaratiladi.
* name, description, va price ustunlari ma'lumotlarni saqlaydi.
* created_at va updated_at maydonlari ma'lumotlar qachon yaratilgan va yangilanganini saqlaydi.
3. schemas.py fayli
Pydantic yordamida ma'lumotlar bazasidagi obyektlarni validatsiya qilish uchun sxemalar yoziladi:
```shell
# app/schemas.py

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ItemCreate(BaseModel):
    name: str
    description: Optional[str]
    price: Decimal

class ItemUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]

class ItemRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: Decimal

    class Config:
        orm_mode = True
```

Tushuntirish:

* ItemCreate — yangi Item obyektini yaratishda ishlatiladigan ma'lumotlarni tekshiradi.
* ItemUpdate — mavjud Item obyektini yangilashda ishlatiladi.
* ItemRead — ma'lumotlarni o'qishda foydalaniladi. orm_mode = True orqali biz ma'lumotlarni ORM (Object-Relational Mapping) obyektlari shaklida qaytaramiz.
4. main.py fayli
Bu faylda asosiy ilova yaratiladi va CRUD amallari (yaratish, o'qish, yangilash, o'chirish) amalga oshiriladi.
```shell
# app/main.py

from fastapi import FastAPI, HTTPException, Depends
from typing import List
from tortoise.contrib.fastapi import register_tortoise
from app import models, schemas

app = FastAPI()

# CRUD uchun funksiyalar

# Yangi item yaratish
@app.post("/items/", response_model=schemas.ItemRead)
async def create_item(item: schemas.ItemCreate):
    item_obj = await models.Item.create(**item.dict())  # Ma'lumotlar bazasida yangi item yaratish
    return item_obj

# Barcha itemlarni o'qish (Read)
@app.get("/items/", response_model=List[schemas.ItemRead])
async def read_items():
    items = await models.Item.all()  # Barcha itemlarni olish
    return items

# ID bo'yicha bitta itemni o'qish
@app.get("/items/{item_id}", response_model=schemas.ItemRead)
async def read_item(item_id: int):
    item = await models.Item.get_or_none(id=item_id)  # ID bo'yicha itemni olish
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Itemni yangilash (Update)
@app.put("/items/{item_id}", response_model=schemas.ItemRead)
async def update_item(item_id: int, item: schemas.ItemUpdate):
    item_obj = await models.Item.get_or_none(id=item_id)  # ID bo'yicha itemni olish
    if not item_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    item_data = item.dict(exclude_unset=True)  # Faqat berilgan ma'lumotlarni yangilash
    for key, value in item_data.items():
        setattr(item_obj, key, value)
    await item_obj.save()
    return item_obj

# Itemni o'chirish (Delete)
@app.delete("/items/{item_id}", response_model=schemas.ItemRead)
async def delete_item(item_id: int):
    item = await models.Item.get_or_none(id=item_id)  # ID bo'yicha itemni olish
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await item.delete()  # Itemni o'chirish
    return item

# Tortoise ORM ni registratsiya qilish
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

```
Tushuntirish:

* create_item — bu funksiya yangi item yaratadi va ma'lumotlar bazasiga saqlaydi. **item.dict() orqali sxema obyektini lug'atga aylantirib, Item.create() yordamida bazaga yoziladi.
* read_items — barcha itemlarni o'qiydi va qaytaradi.
* read_item — bitta itemni ID bo'yicha o'qiydi. Agar item topilmasa, 404 xato qaytaradi.
* update_item — mavjud itemni yangilaydi. exclude_unset=True orqali faqat kiritilgan qiymatlar yangilanadi.
* delete_item — itemni ID bo'yicha o'chiradi va o'chirilgan itemni qaytaradi.
5. Aerich bilan migratsiyalarni boshqarish
Dastlab, aerich yordamida migratsiyalarni yaratib olamiz.

1.  aerich ni boshlash:
```shell
aerich init -t app.config.TORTOISE_ORM
```
2. Dastlabki migratsiyani yaratish:
```shell
aerich init-db

```
6. FastAPI ilovasini ishga tushirish
Ilovani ishga tushiramiz:

```shell
uvicorn app.main:app --reload
```

## Xulosa
Ushbu CRUD dasturi orqali FastAPI yordamida Tortoise ORM bilan ishlashni o'rgandik. Loyihada ma'lumotlar bazasi modeli yaratish (Item), sxemalar (Pydantic) yordamida validatsiya qilish, CRUD operatsiyalarni bajarish (yaratish, o'qish, yangilash, o'chirish) kabi muhim komponentlar o'z aksini topdi.



