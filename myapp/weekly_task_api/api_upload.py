from django.http import JsonResponse
from rest_framework.views import APIView
import aiomysql
import boto3
import asyncio
import logging
from django.conf import settings
from project.asgi import app
from asgiref.sync import async_to_sync
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
s3_client = boto3.client('s3')


async def upload_sql(app, t, url):
    try:
        sql_pool = app.state.async_sql_pool
        async with sql_pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                if url:
                    await cursor.execute("INSERT INTO main_table (text, pic) VALUES (%s, %s);", (t, url))
                else:
                    await cursor.execute("INSERT INTO main_table (text) VALUES (%s);", (t,))
                await connection.commit()
                id = cursor.lastrowid    # 我搞不懂為甚麼 lastrowid 不會亮燈，但是是可用的
                await connection.commit()
                logger.info(id)
                return id
    except Exception as e:
        logger.error(f"SQL upload error: {e}")
        return None

async def upload_s3(pic):
    try:
        file_name = pic.name.replace(' ', '_')
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, s3_client.upload_fileobj, pic, settings.S3_BUCKET, file_name)
        s3_url = f"{settings.CLOUDFRONT_DOMAIN}/{file_name}"
        return s3_url
    except Exception as e:
        logger.error(f"S3 upload error: {e}")
        return None

class UploadTask(APIView):
    def post(self, request, *args, **kwargs):
        return async_to_sync(self.handle_post)(request, *args, **kwargs)
    
    async def handle_post(self, request, *args, **kwargs):
        try:
            t = request.data.get('text')
            pic = request.FILES.get('pic')
            logger.info(t)
            if pic:
                logger.info(f"File name: 52 -> {pic.name}")

            if t:
                url = await upload_s3(pic) if pic else None
                if url:
                    id = await upload_sql(app, t, url)
                    if id:
                        logger.info(f"Data: {id}")
                        return JsonResponse({"status": "success", "message": "Upload successfully"}, status=200)
                    else:
                        return JsonResponse({"status": "error", "message": "SQL upload failed"}, status=500)
                else:
                    return JsonResponse({"status": "error", "message": "S3 upload failed"}, status=500)
            else:
                return JsonResponse({"status": "error", "message": "Must upload at least one piece of msg."}, status=400)
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({"error": str(e)}, status=500)