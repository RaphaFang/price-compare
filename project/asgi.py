import os
import django
import contextlib
from django.core.asgi import get_asgi_application
from myapp.db.sql import build_async_sql_pool, close_async_sql_pool
from starlette.applications import Starlette
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

class AppState:  # 初始化一個附加上去的狀態
    async_sql_pool = None
app_state = AppState()

@contextlib.asynccontextmanager
async def my_lifespan(app):
    try:
        await build_async_sql_pool(app_state)
        app.state = app_state
        logger.info("asgi.py -> connection pool created successfully.")
    except Exception as e:
        logger.error(f"asgi.py -> Failed to create database connection pool: {e}")
    yield
    await close_async_sql_pool(app_state)

app = Starlette(lifespan=my_lifespan)

django_app = get_asgi_application()
app.mount("/", django_app) # 這邊是建立全部的路由中間器

# async def send_startup_signal(app_state):
#     await startup_signal.send(app_state=app_state)

# async def send_shutdown_signal(app_state):
#     await shutdown_signal.send(app_state=app_state)


# @contextlib.asynccontextmanager  # 為甚麼這邊要放一個app？
# async def my_lifespan(app):
#     async with anyio.create_task_group() as task_group:
#         task_group.start_soon(startup_signal.send)
#         yield
#         task_group.start_soon(shutdown_signal.send)

# async def my_lifespan(app):   # 學到yield 第一次發現可以用在這裡，並且寄送一個通知到receiver.py
#     # await build_async_sql_pool(app_state)
#     startup_signal.send(sender=None, app_state=app_state)
#     yield
#     # await close_async_sql_pool(app_state)
#     shutdown_signal.send(sender=None, app_state=app_state)
# # ------------------------------------------------------------
# logger = logging.getLogger(__name__)

# async def this_lifespan(app): # 學到yield 第一次發現可以用在這裡
#     app.async_sql_pool = await build_async_sql_pool()
#     logger.info("start")
#     yield
#     await close_async_sql_pool(app.async_sql_pool)
#     logger.info("end")
# class LifespanMiddleware:
#     def __init__(self, app, lifespan):
#         self.app = app
#         self.lifespan = lifespan

#     async def __call__(self, scope, receive, send):  # 請求類型、接收user請求、向user寄送
#         logger.info("inside call func")

#         if scope['type'] == 'lifespan': # 這只會在開結束時觸發
#             async for message in self.lifespan(self.app): 
#                 await send(message)
#         else:
#             await self.app(scope, receive, send)

# app = LifespanMiddleware(get_asgi_application(), this_lifespan)