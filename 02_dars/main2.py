from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='mini blog site API', version='0.0.1')


class Category(BaseModel):
    name: str


class Tag(BaseModel):
    name: str

class Author(BaseModel):
    name: str
    profession: str
    age: int
    description: str


class Post(BaseModel):
    title: str
    content: str




posts = []

@app.post('/post-create/')
async def create_post(post: Post):
    posts.append(post)
    return {'message': 'Post created successfully'}


@app.get('/post-retrieve/')
async def retrieve_post(post_id: int):
    post = posts[post_id]
    return {'message': post}

@app.put('/post-update/')
async def update_post(post_id: int, post: Post):
    posts[post_id] = post
    return {'message': post}

@app.delete('/post-delete/')
async def delete_post(post_id: int):
    posts.pop(post_id)
    return {'message': 'Post deleted successfully'}

@app.get('/posts/')
async def retrieve_posts():
    return {'posts': posts}


@app.post('/category-create/')
async def create_category(category: Category):
    category.name = category.name
    return {'message': category}

@app.post('/tag-create/')
async def create_tag(tag: Tag):
    posts.append(tag)
    return {'message': tag}


@app.get('/tags/')
async def retrieve_tags():
    return {'tags': posts}

@app.get('/categories/')
async def retrieve_categories():
    return {'categories': posts}

@app.post('/author-create/')
async def create_author(author: Author):
    posts.append(author)
    return {'message': author}