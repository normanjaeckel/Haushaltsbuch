from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class Main(generic.TemplateView):
    template_name = "main.html"


class Overview(LoginRequiredMixin, generic.TemplateView):
    template_name = "overview.html"


class Import(LoginRequiredMixin, generic.TemplateView):
    template_name = "import.html"
