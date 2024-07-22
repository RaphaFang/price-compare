from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@api_view(['POST'])
def upload_task(request):
    try :
        if request.method == 'POST':
            t = request.data.get('text')
            p = request.data.get('pic')
            logger.info(f"Received text: {t}")
            logger.info("--------")
            logger.info(f"Received pic: {p}")

            return Response({"message": "success"}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
