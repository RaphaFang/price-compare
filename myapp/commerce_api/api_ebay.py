# myapp/views.py

from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings


@csrf_exempt
def account_deletion_notification(request):
    if request.method == 'POST':
        token = request.headers.get('verification-token')
        if token != settings.EBAY_VERIFICATION_TOKEN:
            return HttpResponseForbidden('Forbidden')
        
        body = json.loads(request.body)
        print("Received notification:", body)
        return JsonResponse({"message": "Notification received"})
    return HttpResponseForbidden('Forbidden')
