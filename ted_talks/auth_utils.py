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
        if not hasattr(request, 'headers'):
            return JsonResponse({'error': 'Invalid request object, missing headers'}, status=500)

        auth_header = request.headers.get('Authorization', '')
        if not auth_header:
            return JsonResponse({'error': 'No token provided'}, status=401)
        
        try:
            # Check if the token is prefixed with "Token "
            if auth_header.startswith('Token '):
                token = auth_header.split(' ')[1]
            else:
                token = auth_header  # Assume the entire header is the token
            
            api_token = Token.objects.get(key=token)
            request.user = api_token.user
        except (IndexError, Token.DoesNotExist):
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        return view_func(request, *args, **kwargs)
    return wrapped_view