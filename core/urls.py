from django.urls import path

from .consumers import ChatConsumer
from .views import (
    ajax_dislike_user,
    ajax_like_user,
    chat_page_view,
    feed_page_view,
    matches_page_view,
)

urlpatterns = [
    path("", feed_page_view, name="feed_page_view"),
    path("matches/", matches_page_view, name="matches_page_view"),
    path("matches/<str:id>/", chat_page_view, name="chat_page_view"),
    path("ajax/likeuser/", ajax_like_user, name="ajax_like_user"),
    path("ajax/dislikeuser/", ajax_dislike_user, name="ajax_dislike_user"),
]


websocket_urlpatterns = [
    path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()),
]
