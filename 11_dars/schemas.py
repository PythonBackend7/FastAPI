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