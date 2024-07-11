# ted_talks/auth_utils.py
from rest_framework.authtoken.models import Token
from functools import wraps
from django.http import JsonResponse

def create_token_for_user(user):
    token, created = Token.objects.get_or_create(user=user)
    if not created:
        token.delete()
        token = Token.objects.create(user=user)
    return str(token.key)

def token_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Debugging statement to print the type of the request object
        print(f"Request type: {type(request)}")

        if not hasattr(request, 'headers'):
            return JsonResponse({'error': 'Invalid request object, missing headers'}, status=500)

        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'error': 'No token provided'}, status=401)
        try:
            token = token.split(" ")[1]  # Extract token part from "Token <actual-token>"
            api_token = Token.objects.get(key=token)
            request.user = api_token.user
        except (ValueError, Token.DoesNotExist):
            return JsonResponse({'error': 'Invalid token'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapped_view