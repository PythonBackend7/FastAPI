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

@app.patch('/post-update/{post_id}')
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

@app.put('category-update/')
async def update_category(category: Category):
    category.name = category.name
    return {'message': category}

@app.delete('/category-delete/')
async def delete_category(category: Category):
    posts.pop(category.id)
    return {'message': 'Category deleted successfully'}

@app.post('/tag-create/')
async def create_tag(tag: Tag):
    posts.append(tag)
    return {'message': tag}


@app.get('/tags/')
async def retrieve_tags():
    return {'tags': posts}

@app.put('/tag-update/')
async def update_tag(tag_id: int, tag: Tag):
    posts[tag_id] = tag
    return {'message': tag}

@app.delete('/tag-delete/')
async def delete_tag(tag_id: int):
    posts.pop(tag_id)
    return {'message': 'Tag deleted successfully'}

@app.get('/categories/')
async def retrieve_categories():
    return {'categories': posts}

@app.post('/author-create/')
async def create_author(author: Author):
    posts.append(author)
    return {'message': author}


@app.get('/authors/')
async def retrieve_authors():
    return {'authors': posts}

@app.put('/author-update/')
async def update_author(author_id: int, author: Author):
    posts[author_id] = author
    return {'message': author}

@app.patch('/author-update/{author_id}')
async def update_author(author_id: int, author: Author):
    posts[author_id] = author
    return {'message': author}

@app.delete('/author-delete/')
async def delete_author(author_id: int):
    posts.pop(author_id)
    return {'message': 'Author deleted successfully'}
