from .models import Match


def like_count(request):
    if request.user.is_authenticated:
        return {
            "like_count": Match.objects.filter(to=request.user)
            .filter(mode="like")
            .filter(is_matched=False)
            .count()
        }
    return {}
