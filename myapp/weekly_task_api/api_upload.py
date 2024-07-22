from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def upload_task(request):
    try :
        if request.method == 'POST':
            # print("Received data:", request.data)
            t = request.data.get('text')
            p = request.data.get('pic')
            print(t)
            print("--------")
            print(p)

            return Response({"message": "success"}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
