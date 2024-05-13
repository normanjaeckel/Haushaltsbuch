import csv
import datetime

from decimal import Decimal
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from django.db import models
from .models import Booking, Category, Account


class Main(generic.TemplateView):
    template_name = "main.html"


class Overview(LoginRequiredMixin, generic.TemplateView):
    template_name = "overview.html"

    def get_context_data(self, **context):
        year = 2024
        accounts = []
        for category in Category.objects.all():
            for account in category.account_set.all():
                accounts.append(
                    {
                        "name": str(account),
                        "total": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=1, day=1),
                            date__lte=datetime.date(year=year, month=12, day=31),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                        "jan": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=1, day=1),
                            date__lte=datetime.date(year=year, month=1, day=31),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                        "feb": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=2, day=1),
                            date__lte=datetime.date(year=year, month=2, day=29),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                        "mar": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=3, day=1),
                            date__lte=datetime.date(year=year, month=3, day=31),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                        "apr": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=4, day=1),
                            date__lte=datetime.date(year=year, month=4, day=30),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                        "may": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=5, day=1),
                            date__lte=datetime.date(year=year, month=5, day=31),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                        "jun": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=6, day=1),
                            date__lte=datetime.date(year=year, month=6, day=30),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                        "jul": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=7, day=1),
                            date__lte=datetime.date(year=year, month=7, day=31),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                        "aug": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=8, day=1),
                            date__lte=datetime.date(year=year, month=8, day=31),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                        "sep": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=9, day=1),
                            date__lte=datetime.date(year=year, month=9, day=30),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                        "oct": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=10, day=1),
                            date__lte=datetime.date(year=year, month=10, day=31),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                        "nov": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=11, day=1),
                            date__lte=datetime.date(year=year, month=11, day=30),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                        "dec": account.bookings.filter(
                            date__gte=datetime.date(year=year, month=12, day=1),
                            date__lte=datetime.date(year=year, month=12, day=31),
                        ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                    }
                )

        saldo = dict()
        for key in [
            "total",
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
        ]:
            saldo[key] = sum((account[key] for account in accounts))

        context["saldo"] = saldo
        context["accounts"] = accounts
        return super().get_context_data(**context)


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
