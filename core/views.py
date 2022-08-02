from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from .models import Match, Message

User = get_user_model()

# Algorithm to find the best match
def generate_new_user(main_user):
    # get current users all hobbies
    hobbies = main_user.hobbies.all()

    # get only preferred gender
    users = User.objects.filter(gender=main_user.show)

    # get all users with same hobbies
    users = users.filter(hobbies__in=hobbies).distinct()

    # exclude the current user
    users = users.exclude(id=main_user.id)

    # get list of users whom current user have already liked or disliked
    as_liker = main_user.user1.all()
    likee_id = [match.to.id for match in as_liker]

    # get list of users who already have a match with current user
    as_likee = main_user.user2.filter(is_matched=True)
    liker_id = [match.by.id for match in as_likee]

    # exclude the users whom the current user have already liked or disliked
    # and users who already have matched with the current user
    users = users.exclude(id__in=likee_id).exclude(id__in=liker_id)

    # order the user according to their score
    users = users.order_by("-score")

    # return the first user in the list
    new_user = users.first()
    return new_user


@login_required
def feed_page_view(request):
    user = generate_new_user(request.user)
    return render(request, "feed.html", {"user": user})


@login_required
def matches_page_view(request):
    matches = Match.objects.filter(Q(by=request.user) | Q(to=request.user)).filter(
        is_matched=True
    )
    return render(request, "matches.html", {"matches": matches})


@login_required
def chat_page_view(request, id):
    user = User.objects.get(id=id)
    match = (
        Match.objects.filter(Q(by=request.user) | Q(to=request.user))
        .filter(Q(by=user) | Q(to=user))
        .filter(is_matched=True)
        .first()
    )

    chats = (
        Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        .filter(Q(sender=user) | Q(receiver=user))
        .order_by("created_at")
    )
    return render(
        request, "chat.html", {"user": user, "chats": chats, "match_id": match.id}
    )


@login_required
def ajax_like_user(request):
    if request.method == "POST":
        to_user_id = request.POST.get("guestUser")
        to_user = User.objects.get(id=to_user_id)
        by_user = request.user

        if to_user != by_user:
            match_obj = Match.objects.filter(
                by=to_user, to=by_user, mode="like"
            ).first()
            if match_obj:
                match_obj.is_matched = True
                match_obj.save()
                to_user.score += 2
                to_user.save()
                by_user.score += 1
                by_user.save()
            else:
                try:
                    Match.objects.create(by=by_user, to=to_user, mode="like")
                except:
                    pass

    new_user = generate_new_user(request.user)
    if new_user:
        data = {
            "full_name": new_user.full_name,
            "age": new_user.age,
            "bio": new_user.bio,
            "image_url": new_user.profile_photo.url,
            "id": new_user.id,
        }
    else:
        data = {"error": "No more users to like"}
    return JsonResponse(data)


@login_required
def ajax_dislike_user(request):
    if request.method == "POST":
        to_user_id = request.POST.get("guestUser")
        to_user = User.objects.get(id=to_user_id)
        by_user = request.user

        try:
            Match.objects.create(by=by_user, to=to_user, mode="dislike")
        except:
            pass

    new_user = generate_new_user(request.user)
    if new_user:
        data = {
            "full_name": new_user.full_name,
            "age": new_user.age,
            "bio": new_user.bio,
            "image_url": new_user.profile_photo.url,
            "id": new_user.id,
        }
    else:
        data = {"error": "No more users to like"}
    return JsonResponse(data)
