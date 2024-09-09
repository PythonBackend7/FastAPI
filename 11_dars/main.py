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