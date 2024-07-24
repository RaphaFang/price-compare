import aiomysql
from django.conf import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pool = None

async def build_async_sql_pool(app_state):
    try:
        config = settings.DATABASES['default']
        app_state.async_sql_pool = await aiomysql.create_pool(
            host=config['HOST'],
            port=int(config['PORT']),
            user=config['USER'],
            password=config['PASSWORD'],
            db=config['NAME'],
            minsize=1,
            maxsize=10
        )
        logger.info("sql.py ->  connection pool created successfully.")
    except Exception as e:
        logger.error(f"sql.py ->  Error creating database connection pool: {e}")
        raise

async def close_async_sql_pool(app_state):
    if app_state.async_sql_pool:
        app_state.async_sql_pool.close()
        await app_state.async_sql_pool.wait_closed()