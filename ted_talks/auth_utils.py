from django.contrib.auth.models import User
from .models import APIToken  # or from .auth_models import APIToken if you created a separate file
from django.http import JsonResponse
from functools import wraps

def create_token_for_user(user):
    token, created = APIToken.objects.get_or_create(user=user)
    return token.token

def token_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'error': 'No token provided'}, status=401)
        try:
            api_token = APIToken.objects.get(token=token)
            request.user = api_token.user
        except APIToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapped_view