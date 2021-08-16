import asyncio
import requests
import time
from random import shuffle, randint

from fastapi import FastAPI

from config import (
    PHOTOS_LIST_TIME,
    DETAIL_PHOTO_TIME,
    POSTS_LIST_TIME,
    DETAIL_POST_TIME,
)

app = FastAPI()


def get_data(query: str):
    data = requests.get(f'http://jsonplaceholder.typicode.com/{query}').json()
    if data:
        shuffle(data)
        return data
    return {'result': 'wrong query!'}


@app.get('/photos/')
async def photos_list():
    time.sleep(PHOTOS_LIST_TIME)
    return get_data('photos')


@app.get('/photos/{id}')
async def detail_photo(id: int):
    time.sleep(DETAIL_PHOTO_TIME)
    if id not in range(len(get_data('photos'))):
        return {'result': 'wrong id!'}
    return get_data('photos')[id-1]


@app.get('/posts')
async def posts_list():
    time.sleep(POSTS_LIST_TIME)
    return get_data('posts')


@app.get('/posts/{id}')
async def detail_post(id: int):
    time.sleep(DETAIL_POST_TIME)
    if id not in range(len(get_data('posts'))):
        return {'result': 'wrong id!'}
    return get_data('posts')[id-1]


@app.get('/')
async def home():
    detail_photo_id = randint(1, len(get_data('photos')))
    detail_post_id = randint(1, len(get_data('posts')))
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
