from django.urls import path
from core.views import IndexPageView


urlpatterns = [
    path('', IndexPageView.as_view(), name='index_page'),
]
