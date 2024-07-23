from django.http import JsonResponse
from rest_framework.decorators import api_view
import aiomysql
from project.asgi import app
import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3_client = boto3.client('s3')

@api_view(['POST'])
def upload_task(request):
    try :
        if request.method == 'POST':
            t = request.data.get('text')
            pic = request.FILES.get('pic')
            def upload_s3(pic):  # 這邊我不是用非同步處理，
                try:
                    file_name = pic.name
                    s3_client.upload_fileobj(pic, settings.S3_BUCKET, file_name)
                    s3_url = f"https://{settings.CLOUDFRONT_DOMAIN}/{file_name}"
                    return s3_url
                except Exception as e:
                    return JsonResponse({"error": str(e)}, status=500)

            async def upload_sql(t,url):
                sql_pool = app.async_sql_pool 
                async with sql_pool.acquire() as connection:
                    async with connection.cursor(aiomysql.DictCursor) as cursor:
                        if url:
                            await cursor.execute("INSERT INTO main_table (text, pic) VALUES (%s, %s);", (t,url,)) 
                        else:
                            await cursor.execute("INSERT INTO main_table (text) VALUES (%s);", (t,))
                        data =  await cursor.fetchone()
                        return data
            if t:
                url = upload_s3(pic) if pic else None
                data = upload_sql(t,url)
                return JsonResponse({"status":"success","message": "Upload successfully"}, status=200)

            else:
                return JsonResponse({"status":"error","message": ""}, status=400)

    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
    
