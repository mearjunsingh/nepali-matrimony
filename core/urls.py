from django.urls import path
from core.views import feed_page_view, ajax_like_user, ajax_dislike_user


urlpatterns = [
    path('', feed_page_view, name='feed_page_view'),
    path('ajax/likeuser/', ajax_like_user, name='ajax_like_user'),
    path('ajax/dislikeuser/', ajax_dislike_user, name='ajax_dislike_user'),
]
