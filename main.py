import asyncio
from random import shuffle, randint

from aiohttp import ClientSession
from fastapi import FastAPI

from config import (
    PHOTOS_LIST_TIME,
    DETAIL_PHOTO_TIME,
    POSTS_LIST_TIME,
    DETAIL_POST_TIME,
)

app = FastAPI()


async def main(query):
    async with ClientSession() as session:
        url = f'http://jsonplaceholder.typicode.com/{query}'
        async with session.get(url) as response:
            if response.status != 200:
                return {'result': 'wrong query!'}
            data = await response.json()
            shuffle(data)
            return data


@app.get('/photos/')
async def photos_list():
    await asyncio.sleep(PHOTOS_LIST_TIME)
    return await main('photos')


@app.get('/photos/{id}')
async def detail_photo(id: int):
    await asyncio.sleep(DETAIL_PHOTO_TIME)
    photos = await main('photos')
    if id not in range(len(photos)):
        return {'result': 'wrong id!'}
    return photos[id]


@app.get('/posts')
async def posts_list():
    await asyncio.sleep(POSTS_LIST_TIME)
    return await main('posts')


@app.get('/posts/{id}')
async def detail_post(id: int):
    await asyncio.sleep(DETAIL_POST_TIME)
    posts = await main('posts')
    if id not in range(len(posts)):
        return {'result': 'wrong id!'}
    return posts[id]


@app.get('/')
async def home():
    photos = await main('photos')
    posts = await main('posts')
    detail_photo_id = randint(0, len(photos) - 1)
    detail_post_id = randint(0, len(posts) - 1)
    futures = [
        photos_list(),
        detail_photo(detail_photo_id),
        posts_list(),
        detail_post(detail_post_id),
    ]
    photos, photo, posts, post = await asyncio.gather(*futures)
    return {
        'photos_list': photos,
        'detail_photo': photo,
        'posts_list': posts,
        'detail_post': post,
    }
