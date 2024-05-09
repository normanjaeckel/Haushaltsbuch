from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"

    def __str__(self):
        return self.name


class Account(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Konto"
        verbose_name_plural = "Konten"

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Booking(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    senderRecipient = models.CharField(max_length=255)
    reference = models.TextField()
    date = models.DateField()

    class Meta:
        verbose_name = "Buchung"
        verbose_name_plural = "Buchungen"

    def __str__(self):
        return f"{self.date} – {self.amount} Euro – {self.account}"


class Reserve(models.Model):
    name = models.CharField(max_length=255, unique=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Rücklage"
        verbose_name_plural = "Rücklagen"

    def __str__(self):
        return f"{self.name} – EUR {self.amount} p. M. / EUR {12*self.amount} p. a. – {self.account}"
