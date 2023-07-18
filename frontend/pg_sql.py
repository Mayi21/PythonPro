import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import fields, models

from backend.db_util import User

app = FastAPI()

register_tortoise(
    app,
    db_url=os.getenv('db_url'),
    modules={'models': [models]}
)


@app.get('/users')
async def get_users():
    return await User.all()


if __name__ == '__main__':
    os.system('uvicorn pg_sql:app --reload')
