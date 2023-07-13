import os

from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise

# 创建 FastAPI 应用程序
app = FastAPI()

db_address = os.getenv("db_address")
db_name = os.getenv("db_name")
db_username = os.getenv("db_username")

# 定义模型
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password = fields.CharField(128)

    class Meta:
        table = "users"

# 连接到数据库
async def init_db():
    await Tortoise.init(
        db_url="sqlite://:memory:",  # 根据实际情况修改数据库连接字符串
        modules={"models": ["__main__"]},
    )
    await Tortoise.generate_schemas()

# 注册 Tortoise ORM 到 FastAPI
register_tortoise(
    app,
    db_url="sqlite://:memory:",  # 根据实际情况修改数据库连接字符串
    modules={"models": ["__main__"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

# 路由和处理程序
@app.post("/users")
async def create_user(username: str, password: str):
    user = await User.create(username=username, password=password)
    return {"id": user.id, "username": user.username}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if user:
        return {"id": user.id, "username": user.username}
    else:
        return {"message": "User not found"}

# 启动应用程序时初始化数据库连接
@app.on_event("startup")
async def startup_event():
    await init_db()

# 关闭应用程序时关闭数据库连接
@app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()

# 运行 FastAPI 应用程序
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
