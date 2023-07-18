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
    username = fields.CharField(50, unique=True)
    class Meta:
        table = "user"

# 连接到数据库
async def init_db():
    await Tortoise.init(
        db_url="postgresql://47.100.38.198:5433/dbd7a9034608ad4a6695fe9ca49984b24fwechat",  # 根据实际情况修改数据库连接字符串
        modules={"models": ["__main__"]},
    )
    await Tortoise.generate_schemas()

# 注册 Tortoise ORM 到 FastAPI
register_tortoise(
    app,
    db_url="postgresql://47.100.38.198:5433/dbd7a9034608ad4a6695fe9ca49984b24fwechat",  # 根据实际情况修改数据库连接字符串
    modules={"models": ["__main__"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

# 路由和处理程序
@app.post("/users")
async def get_user():
    user = User.get()
    print(user)

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
    os.system("uvicorn orm_framework:app --reload")
