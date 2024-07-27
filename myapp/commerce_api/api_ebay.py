# myapp/views.py

from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
import hashlib



@csrf_exempt
def account_deletion_notification(request):
    if request.method == 'POST':
        token = request.headers.get('verification-token')
        if token != settings.EBAY_VERIFICATION_TOKEN:
            return HttpResponseForbidden('Forbidden')
        
        body = json.loads(request.body)
        print("Received notification:", body)
        return JsonResponse({"message": "Notification received"})
    
    elif request.method == 'GET':
        challenge_code = request.GET.get('challenge_code')
        if not challenge_code:
            return HttpResponseForbidden('Forbidden')
        
        verification_token = settings.EBAY_VERIFICATION_TOKEN
        endpoint = "https://raphaelfang.com/pc/v1/ebay/deletion/"
        combined_string = challenge_code + verification_token + endpoint
        hashed_value = hashlib.sha256(combined_string.encode()).hexdigest()
        
        return JsonResponse({"challengeResponse": hashed_value})
    
    return HttpResponseForbidden('Forbidden')