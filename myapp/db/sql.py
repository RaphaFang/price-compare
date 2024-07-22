import aiomysql
from django.conf import settings

async def build_async_sql_pool():
    config = settings.DATABASES['sql_task']
    pool = await aiomysql.create_pool(
        host=config['HOST'],
        port=int(config['PORT']),
        user=config['USER'],
        password=config['PASSWORD'],
        db=config['NAME'],
        minsize=1,
        maxsize=10
    )
    return pool

async def close_async_sql_pool(pool):
    pool.close()
    await pool.wait_closed()