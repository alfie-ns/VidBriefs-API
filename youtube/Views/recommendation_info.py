from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from ..models import Video, UserInteraction

@require_http_methods(["GET"])
def recommendation_info(request, user_id):
    try:
        # Implement your recommendation logic here
        # This is a placeholder logic
        recommendations = Video.objects.all()[:10]  # Example: get the first 10 videos

        # Convert recommendations to a suitable format
        recommendations_data = [{'video_id': video.video_id, 'title': video.title} for video in recommendations]

        return JsonResponse({'recommendations': recommendations_data}, status=200)

    except Exception as e:
        # Handle exceptions
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
