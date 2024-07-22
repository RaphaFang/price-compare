from django.http import JsonResponse
from rest_framework.decorators import api_view
import aiomysql
from project.asgi import app

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@api_view(['GET'])
def download_task(request):
    try :
        if request.method == 'GET':
            # async def upload_sql(request,t,p):
            #     sql_pool = app.async_sql_pool 
            #     async with sql_pool.acquire() as connection:
            #         async with connection.cursor(aiomysql.DictCursor) as cursor:
            #             await cursor.execute("SELECT * FROM main_table WHERE email = %s AND password = %s AND auth_provider IS NULL;", (e,p,)) 
            #             data =  await cursor.fetchone()

            logger.info('Great, just test setup.')

            # if p:
            #     logger.info(f"Received pic: {p.name}")

            # else:
            #     logger.info("No picture uploaded")

            return JsonResponse({"message": 'Great, just test setup.'}, status=200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
