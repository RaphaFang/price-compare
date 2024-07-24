from django.http import JsonResponse
from rest_framework.decorators import APIView
import aiomysql
import boto3
from project.asgi import app
from asgiref.sync import async_to_sync
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
s3_client = boto3.client('s3')

async def download_sql(app):
    try:
        sql_pool = app.state.async_sql_pool
        async with sql_pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM main_table ORDER BY created_at DESC LIMIT 10;")
                data = await cursor.fetchall()
                return data
            
    except Exception as e:
        logger.error(f"SQL download error: {e}")
        return None

class DownloadTask(APIView):
    def get(self, request, *args, **kwargs):
        return async_to_sync(self.handle_get)()
    
    async def handle_get(self):
        try:
            data = await download_sql(app)
            if not data:
                return JsonResponse({"status": "error", "message": "SQL download failed"}, status=500)
            return JsonResponse({"status": "success","data":data}, status=200)

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({"error": str(e)}, status=500)