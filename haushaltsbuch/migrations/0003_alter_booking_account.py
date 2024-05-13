# Generated by Django 5.0.6 on 2024-05-13 20:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("haushaltsbuch", "0002_add_defaults"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="account",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="bookings",
                to="haushaltsbuch.account",
            ),
        ),
    ]