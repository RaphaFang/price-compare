import os
from django.core.asgi import get_asgi_application
from myapp.db.sql import build_async_sql_pool, close_async_sql_pool

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = get_asgi_application()

# async def startup(app):
#     app.async_sql_pool = await build_async_sql_pool()
# async def shutdown(app):
#     await close_async_sql_pool(app.async_sql_pool)

async def lifespan(app): # 學到yield 第一次發現可以用在這裡
    app.async_sql_pool = await build_async_sql_pool()
    yield
    await close_async_sql_pool(app.async_sql_pool)
class LifespanMiddleware:
    def __init__(self, app, lifespan):
        self.app = app
        self.lifespan = lifespan

    async def __call__(self, scope, receive, send):  # 請求類型、接收user請求、向user寄送
        if scope['type'] == 'lifespan': # 這只會在開結束時觸發
            async for message in self.lifespan(self.app): 
                await send(message)
        else:
            await self.app(scope, receive, send)

app = LifespanMiddleware(app, lifespan)