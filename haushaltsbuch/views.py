import calendar
import csv
import datetime
from decimal import Decimal

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.urls import reverse_lazy
from django.views import generic

from .models import Account, Booking, Category, Correcture, Reserve


class Main(generic.TemplateView):
    template_name = "main.html"


class Overview(LoginRequiredMixin, generic.TemplateView):
    template_name = "overview.html"

    month_list = [
        ("jan", 1),
        ("feb", 2),
        ("mar", 3),
        ("apr", 4),
        ("may", 5),
        ("jun", 6),
        ("jul", 7),
        ("aug", 8),
        ("sep", 9),
        ("oct", 10),
        ("nov", 11),
        ("dec", 12),
    ]

    def get_context_data(self, **context):
        year = 2024

        correctures = {
            "total": Correcture.objects.filter(
                date__gte=datetime.date(year=year, month=1, day=1),
                date__lte=datetime.date(year=year, month=12, day=31),
            ).aggregate(models.Sum("amount", default=0))["amount__sum"],
        }
        for month, i in self.month_list:
            correctures[month] = Correcture.objects.filter(
                date__gte=datetime.date(year=year, month=i, day=1),
                date__lte=datetime.date(
                    year=year, month=i, day=calendar.monthrange(year, i)[1]
                ),
            ).aggregate(models.Sum("amount", default=0))["amount__sum"]

        accounts = []
        for category in Category.objects.all():
            for account in category.account_set.all():
                element = {
                    "name": str(account),
                    "total": account.bookings.filter(
                        date__gte=datetime.date(year=year, month=1, day=1),
                        date__lte=datetime.date(year=year, month=12, day=31),
                    ).aggregate(models.Sum("amount", default=0))["amount__sum"],
                }
                for month, i in self.month_list:
                    element[month] = account.bookings.filter(
                        date__gte=datetime.date(year=year, month=i, day=1),
                        date__lte=datetime.date(
                            year=year, month=i, day=calendar.monthrange(year, i)[1]
                        ),
                    ).aggregate(models.Sum("amount", default=0))["amount__sum"]
                accounts.append(element)

        reserves = []
        for reserve in Reserve.objects.all():
            element = {
                "name": str(reserve),
                "total": -reserve.bookings.filter(
                    date__gte=datetime.date(year=year, month=1, day=1),
                    date__lte=datetime.date(year=year, month=12, day=31),
                ).aggregate(models.Sum("amount", default=0))["amount__sum"],
            }
            for month, i in self.month_list:
                if Booking.objects.filter(
                    date__gte=datetime.date(year=year, month=i, day=1)
                ).exists():
                    value = reserve.amount
                    value += reserve.bookings.filter(
                        date__gte=datetime.date(year=year, month=i, day=1),
                        date__lte=datetime.date(
                            year=year, month=12, day=calendar.monthrange(year, i)[1]
                        ),
                    ).aggregate(models.Sum("amount", default=0))["amount__sum"]
                    element["total"] -= reserve.amount
                else:
                    value = 0
                element[month] = value * -1
            reserves.append(element)

        saldo = {
            "total": sum((account["total"] for account in accounts))
            + correctures["total"]
            + sum((reserve["total"] for reserve in reserves)),
        }
        for month, _ in self.month_list:
            saldo[month] = (
                sum((account[month] for account in accounts))
                + correctures[month]
                + sum((reserve[month] for reserve in reserves))
            )

        context["saldo"] = saldo
        context["correctures"] = correctures
        context["accounts"] = accounts
        context["reserves"] = reserves
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
