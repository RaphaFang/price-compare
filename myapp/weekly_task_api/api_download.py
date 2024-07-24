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
                await cursor.execute("SELECT * from main_table;")
                data = await cursor.fetchall()

                logger.info(data)
                return data
            
    except Exception as e:
        logger.error(f"SQL download error: {e}")
        return None

class DownloadTask(APIView):
    def get(self, request, *args, **kwargs):
        return async_to_sync(self.handle_get)(request, *args, **kwargs)
    
    async def handle_get(self, request, *args, **kwargs):
        try:
            data = await download_sql(app)
            if data:
                # logger.info(f"Data: {data}")
                return JsonResponse({"status": "success","data":data}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "SQL download failed"}, status=500)

            # if t:
            #     url = await upload_s3(pic) if pic else None
            #     if url:
            #         id = await download_sql(app)
            #         if id:
            #             logger.info(f"Data: {id}")
            #             return JsonResponse({"status": "success", "message": "Upload successfully"}, status=200)
            #         else:
            #             return JsonResponse({"status": "error", "message": "SQL upload failed"}, status=500)
            #     else:
            #         return JsonResponse({"status": "error", "message": "S3 upload failed"}, status=500)
            # else:
            #     return JsonResponse({"status": "error", "message": "Must upload at least one piece of msg."}, status=400)
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({"error": str(e)}, status=500)