# Clark Portfolio website created by fastapi and tortoise-orm
 Sayt loyihasi:
```shell
project_nome
  |_
    |_database.py
    |_models.py
    |_main.py
    |_schemas.py
``` 

1. Database faylini yaratamiz va quyidagi kodlarni yozamiz.
```shell
from tortoise import Tortoise, fields
from tortoise.models import Model

TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3"  # SQLite ma'lumotlar bazasi
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # `models` - bizning modellar
            "default_connection": "default",
        }
    },
}

async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
```

2. models.py - Model yaratish
```shell
from tortoise import fields, models

class About(models.Model):
    name = fields.CharField(max_length=100)
    birthday = fields.DateField()
    address = fields.CharField(max_length=255)
    email = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=20)
    project_count = fields.IntField()
    cv = fields.CharField(max_length=255)

class Resume(models.Model):
    start_year = fields.IntField()
    finish_year = fields.IntField()
    profession = fields.CharField(max_length=100)
    university = fields.CharField(max_length=255)
    description = fields.TextField()

class Service(models.Model):
    image = fields.CharField(max_length=255)
    title = fields.CharField(max_length=100)
    link = fields.CharField(max_length=255)
    price = fields.FloatField()

class Skill(models.Model):
    name = fields.CharField(max_length=100)
    percentage = fields.IntField()

class Project(models.Model):
    image = fields.CharField(max_length=255)
    link = fields.CharField(max_length=255)
    title = fields.CharField(max_length=100)

class Category(models.Model):
    name = fields.CharField(max_length=100)

class Tag(models.Model):
    name = fields.CharField(max_length=100)

class Post(models.Model):
    title = fields.CharField(max_length=255)
    image = fields.CharField(max_length=255)
    description = fields.TextField()
    author_name = fields.CharField(max_length=100)
    category = fields.ForeignKeyField("models.Category", related_name="posts")
    tags = fields.ManyToManyField("models.Tag", related_name="posts")

class Contact(models.Model):
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100)
    website = fields.CharField(max_length=255)
    message = fields.TextField()

```
3. schemas.py - Pydantic schemas
```shell
from pydantic import BaseModel
from typing import List, Optional

# About schemas
class AboutBase(BaseModel):
    name: str
    birthday: str
    address: str
    email: str
    phone: str
    project_count: int
    cv: str

class AboutCreate(AboutBase):
    pass

class About(AboutBase):
    id: int
    class Config:
        orm_mode = True

# Resume schemas
class ResumeBase(BaseModel):
    start_year: int
    finish_year: int
    profession: str
    university: str
    description: str

class ResumeCreate(ResumeBase):
    pass

class Resume(ResumeBase):
    id: int
    class Config:
        orm_mode = True

# Service schemas
class ServiceBase(BaseModel):
    image: str
    title: str
    link: str
    price: float

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int
    class Config:
        orm_mode = True

# Skill schemas
class SkillBase(BaseModel):
    name: str
    percentage: int

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    class Config:
        orm_mode = True

# Project schemas
class ProjectBase(BaseModel):
    image: str
    link: str
    title: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    class Config:
        orm_mode = True

# Category schemas
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True

# Tag schemas
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    class Config:
        orm_mode = True

# Post schemas
class PostBase(BaseModel):
    title: str
    image: str
    description: str
    author_name: str

class PostCreate(PostBase):
    category_id: int
    tag_ids: List[int]

class Post(PostBase):
    id: int
    category: Category
    tags: List[Tag] = []

    class Config:
        orm_mode = True

# Contact schemas
class ContactBase(BaseModel):
    name: str
    email: str
    website: str
    message: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    class Config:
        orm_mode = True

```
4. main.py - FastAPI yo'llari
```shell
from fastapi import FastAPI, HTTPException, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from typing import List
from models import About, Resume, Service, Skill, Project, Category, Tag, Post, Contact
import schemas

app = FastAPI()

# Dependency
def get_db():
    pass  # SQLite bilan ishlayotganimiz uchun ma'lumotlar bazasini to'g'ridan-to'g'ri bog'laymiz.

# About CRUD
@app.get("/about/", response_model=List[schemas.About])
async def get_about():
    return await About.all()

@app.post("/about/", response_model=schemas.About)
async def create_about(about: schemas.AboutCreate):
    new_about = await About.create(**about.dict())
    return new_about

# Resume CRUD
@app.get("/resume/", response_model=List[schemas.Resume])
async def get_resume():
    return await Resume.all()

@app.post("/resume/", response_model=schemas.Resume)
async def create_resume(resume: schemas.ResumeCreate):
    new_resume = await Resume.create(**resume.dict())
    return new_resume

# Service CRUD
@app.get("/services/", response_model=List[schemas.Service])
async def get_services():
    return await Service.all()

@app.post("/services/", response_model=schemas.Service)
async def create_service(service: schemas.ServiceCreate):
    new_service = await Service.create(**service.dict())
    return new_service

# Skill CRUD
@app.get("/skills/", response_model=List[schemas.Skill])
async def get_skills():
    return await Skill.all()

@app.post("/skills/", response_model=schemas.Skill)
async def create_skill(skill: schemas.SkillCreate):
    new_skill = await Skill.create(**skill.dict())
    return new_skill

# Project CRUD
@app.get("/projects/", response_model=List[schemas.Project])
async def get_projects():
    return await Project.all()

@app.post("/projects/", response_model=schemas.Project)
async def create_project(project: schemas.ProjectCreate):
    new_project = await Project.create(**project.dict())
    return new_project

# Category CRUD
@app.get("/categories/", response_model=List[schemas.Category])
async def get_categories():
    return await Category.all()

@app.post("/categories/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate):
    new_category = await Category.create(**category.dict())
    return new_category

# Tag CRUD
@app.get("/tags/", response_model=List[schemas.Tag])
async def get_tags():
    return await Tag.all()

@app.post("/tags/", response_model=schemas.Tag)
async def create_tag(tag: schemas.TagCreate):
    new_tag = await Tag.create(**tag.dict())
    return new_tag

# Post CRUD
@app.get("/posts/", response_model=List[schemas.Post])
async def get_posts():
    return await Post.all().prefetch_related("category", "tags")

@app.post("/posts/", response_model=schemas.Post)
async def create_post(post: schemas.PostCreate):
    new_post = await Post.create(**post.dict(exclude={"tag_ids"}))
    tags = await Tag.filter(id__in=post.tag_ids)
    await new_post.tags.add(*tags)
    return new_post

# Contact CRUD
@app.post("/contact/", response_model=schemas.Contact)
async def create_contact(contact: schemas.ContactCreate):
    new_contact = await Contact.create(**contact.dict())
    return new_contact

# Tortoise ORM'ni FastAPI bilan bog'lash
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

```

### API xulosasi:

#### 1. Modellar: Har bir model (About, Resume, Service, Skill, Project, Category, Tag, Post, Contact) Tortoise-ORM yordamida yaratilgan. Ushbu modellar FastAPI yordamida CRUD operatsiyalarini bajarishga imkon beradi. Tortoise-ORM bilan ishlaganda, modeldagi ma'lumotlar bazasi bog'lanishi (foreign keys, many-to-many) kabi xususiyatlarni qulay boshqarish mumkin.

#### 2. Pydantic schemas: API orqali kiruvchi va chiquvchi ma'lumotlarni boshqarish uchun Pydantic schema-laridan foydalanilgan. Schema-lar ma'lumotlar modelini aks ettiradi va ular yordamida ma'lumotlar validatsiyasi amalga oshiriladi.

* Base schemas: Har bir model uchun asosiy ma'lumotlar strukturasini aks ettiradi. Masalan, AboutBase da name, birthday, address kabi maydonlar bor.
* Create schemas: CRUD uchun create operatsiyalarida foydalaniladigan schema-lar (masalan, AboutCreate, PostCreate).
* Response schemas: Ma'lumot bazasidan olinadigan yoki qaytariladigan ma'lumotlar uchun schema-lar (About, Post). ORM-rejim (orm_mode = True) orqali model obyektlarini bevosita ma'lumotlar bazasidan Pydantic schema-ga aylantirish mumkin.
#### 3. CRUD operatsiyalari:

* GET: Har bir model uchun GET yo'li orqali barcha obyektlarni olish. Masalan, @app.get("/about/") orqali barcha About obyektlarini olish.
* POST: Yangi obyekt yaratish uchun POST yo'llari. Masalan, @app.post("/about/") orqali yangi About obyektini yaratish mumkin.
*  M2M bog'lanishlar: Post modeli orqali category va tags ko'pdan-ko'p munosabatlari amalga oshiriladi. PostCreate schema-sida category_id va tag_ids orqali Post ni Category va Tag bilan bog'lash.
#### 4. Validatsiya: Pydantic orqali kiruvchi ma'lumotlar validatsiya qilinadi. Masalan, email maydoni noto'g'ri formatda kiritilsa, FastAPI avtomatik ravishda xatolik qaytaradi.

#### 5. Prefetching: Tortoise ORM’da prefetch_related yordamida bog‘langan modellarni oldindan yuklash imkoniyati mavjud. Masalan, Post modeli category va tags bilan bog'langan, shuning uchun @app.get("/posts/") so'roviga prefetch_related("category", "tags") bilan barcha kerakli ma'lumotlarni birgalikda olish mumkin.

#### 6. Tortoise ORM bilan integratsiya: FastAPI bilan birgalikda ishlash uchun register_tortoise yordamida Tortoise ORM sozlangan. Bu integratsiya orqali avtomatik ravishda ma'lumotlar bazasi sxemalarini yaratish, va istisno handler-lar bilan ishlash amalga oshiriladi. Har bir yo'lni bog'lash uchun app obyektiga Tortoise ORM qo'shilgan.

#### 7. SQLite ma'lumotlar bazasi: Ushbu loyiha uchun SQLite bazasi tanlangan, lekin kerak bo'lsa boshqa DBMS-lar bilan ham ishlash uchun konfiguratsiyani moslashtirish mumkin.

#### 8. Ko'p maydonli (Many-to-Many) va bir-biriga bog'langan (Foreign Key) munosabatlar:

* Post modeli Category va Tag modellariga bog‘langan.
* Many-to-Many: Post va Tag orasidagi ko'pdan-ko'p bog'lanish amalga oshiriladi.
* Foreign Key: Post va Category orasida to'g'ridan-to'g'ri bog'lanish mavjud, ya'ni har bir post ma'lum bir kategoriyaga tegishli bo'ladi.
#### 9. Avtomatik sxema yaratish: register_tortoise yordamida, Tortoise ORM avtomatik ravishda ma'lumotlar bazasi sxemalarini (tables) yaratadi.

### Umuman olganda, ushbu API:

* Ma'lumotlar bazasida CRUD operatsiyalarni bajarish uchun FastAPI va Tortoise ORM dan foydalangan.
* Pydantic orqali kiruvchi va chiquvchi ma'lumotlar validatsiyasi va boshqaruvi ta'minlangan.
* Django ORM yoki SQLAlchemy kabi boshqa ORM'lar bilan ishlash tajribasiga o'xshash tarzda Tortoise ORM bilan samarali API yaratildi.

