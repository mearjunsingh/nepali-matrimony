from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexPageView(LoginRequiredMixin, TemplateView):
    pass