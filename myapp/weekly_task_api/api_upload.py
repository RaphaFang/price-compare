from django.http import JsonResponse
from rest_framework.decorators import api_view
import aiomysql
from project.asgi import app

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@api_view(['POST'])
def upload_task(request):
    try :
        if request.method == 'POST':
            t = request.data.get('text')
            p = request.FILES.get('pic')

            async def read_pic():
                with open("/path/to/your/image.jpg", "rb") as file:
                    binary_data = file.read()

            async def upload_sql(request,t,p):
                sql_pool = app.async_sql_pool 
                async with sql_pool.acquire() as connection:
                    async with connection.cursor(aiomysql.DictCursor) as cursor:
                        await cursor.execute("INSERT INTO main_table (text, pic) VALUES (%s, %s);", (t,p,)) 

                        data =  await cursor.fetchone()
                        return data

            logger.info(t)

            # if t:
            #     data = await upload_sql(request,t,p)
            # else:
            #     pass
            

            if p:
                logger.info(f"Received pic: {p.name}")
            else:
                logger.info("No picture uploaded")

            return JsonResponse({"message": "success"}, status=200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
    
