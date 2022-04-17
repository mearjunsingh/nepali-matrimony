from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from core.models import Like


User = get_user_model()


@login_required
def feed_page_view(request):
    user = User.objects.get(phone_number=98)
    return render(request, 'feed.html', {'user': user})


@login_required
def ajax_like_user(request):
    # prev_user_id = request.POST.get('guestUser')
    # prev_user = User.objects.get(id=prev_user_id)
    # curr_user = request.user
    # if prev_user.id != curr_user.id:
    #     if Like.objects.filter(by=curr_user, to=prev_user).exists():
    #         return JsonResponse({'is_match': True})
    #     else:
    #         Like.objects.create(by=curr_user, to=prev_user)
    
    #todo
    import random

    user = User.objects.all()
    new_user = random.choice(user)
    data = {
        'full_name': new_user.full_name,
        'age': new_user.age,
        'bio': new_user.bio,
        'image_url': new_user.profile_photo.url,
        'id': new_user.id
    }
    return JsonResponse(data)


@login_required
def ajax_dislike_user(request):
    # prev_user_id = request.POST.get('guestUser')
    
    import random
    user = User.objects.all()
    new_user = random.choice(user)
    data = {
        'full_name': new_user.full_name,
        'age': new_user.age,
        'bio': new_user.bio,
        'image_url': new_user.profile_photo.url,
        'id': new_user.id
    }
    return JsonResponse(data)