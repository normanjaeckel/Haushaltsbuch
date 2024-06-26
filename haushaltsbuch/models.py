from django.db import models
from django.forms import ModelForm


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    weight = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"
        ordering = ["weight"]

    def __str__(self):
        return self.name


class Account(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    weight = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Konto"
        verbose_name_plural = "Konten"
        ordering = ["category", "weight"]
        unique_together = [["category", "name"]]

    def __str__(self):
        return f"{self.category.name}: {self.name}"


class Reserve(models.Model):
    name = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Rücklage"
        verbose_name_plural = "Rücklagen"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} – EUR {self.amount} p. M. / EUR {12*self.amount} p. a."


class Booking(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="bookings",
    )
    date = models.DateField()
    payment_party = models.CharField(max_length=255)
    banking_text = models.CharField(max_length=255)
    reference = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    additional_information = models.TextField(blank=True)
    reserve = models.ForeignKey(
        Reserve,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="bookings",
    )

    class Meta:
        verbose_name = "Buchung"
        verbose_name_plural = "Buchungen"
        ordering = ["date"]

    def __str__(self):
        if self.account is not None:
            return f"{self.date} | {self.amount} Euro | {self.account.category.name}: {self.account.name}"
        return f"{self.date} | {self.amount} Euro | Noch nicht gebucht"

    def text(self):
        return f"{self.banking_text} | {self.payment_party} | {self.reference}"


class Correcture(models.Model):
    date = models.DateField()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Ein positiver Betrag bedeutet, dass wir eine Erstattung z. B. in bar erhalten haben.",
    )
    description = models.TextField()

    class Meta:
        verbose_name = "Korrektur"
        verbose_name_plural = "Korrekturen"

    def __str__(self):
        return f"{self.date} | {self.amount} Euro | {self.description}"
