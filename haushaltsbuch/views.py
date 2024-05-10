import csv
import datetime

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .models import Booking


class Main(generic.TemplateView):
    template_name = "main.html"


class Overview(LoginRequiredMixin, generic.TemplateView):
    template_name = "overview.html"


class ImportForm(forms.Form):
    csvfile = forms.FileField()


class Import(LoginRequiredMixin, generic.FormView):
    template_name = "import.html"
    form_class = ImportForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        csv_file = form.cleaned_data["csvfile"]
        csv_string = csv_file.read().decode()
        data = csv.DictReader(csv_string.split("\n"), delimiter=";")
        for booking in data:
            b = Booking(
                date=transform_date(booking["Buchungstag"]),
                payment_party=booking["Name Zahlungsbeteiligter"],
                banking_text=booking["Buchungstext"],
                reference=booking["Verwendungszweck"],
                amount=transform_amount(booking["Betrag"]),
            )
            b.save()
        return super().form_valid(form)


def transform_date(date):
    d = date.split(".")
    return datetime.date(int(d[2]), int(d[1]), int(d[0]))


def transform_amount(amount):
    return amount.replace(",", ".")
