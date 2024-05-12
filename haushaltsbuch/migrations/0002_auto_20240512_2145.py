# Generated by Django 5.0.6 on 2024-05-12 21:45

from collections import OrderedDict

from django.db import migrations


def get_defaults():
    d = OrderedDict()
    d["Einnahmen"] = ["Gehalt", "Kindergeld", "Sonstiges"]
    d["Geld"] = ["Bargeld", "Umbuchung Kreditkarte"]
    d["Wohnen und Medien"] = ["Miete", "Strom", "Festnetz, Handy"]
    d["Täglicher Bedarf"] = ["Lebensmittel", "Kleidung", "Gesundheit", "Sonstiges"]
    d["Vorsorge, Versicherung"] = [
        "Riesterrente",
        "Fonds (Oskar.de)",
        "Risikoversicherungen",
    ]
    d["Kinder"] = ["Schule", "Kinderbetreuung", "Mittagessen"]
    d["Musik"] = ["Eltern", "Kinder"]
    d["Freizeit"] = ["Ausflüge", "Spiele, Spielzeug"]
    d["Urlaub"] = ["Sommer", "Rüstzeiten"]
    d["Spenden"] = ["Christlich", "Parteien", "Sonstiges"]
    return d


def add_defaults(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Category = apps.get_model("haushaltsbuch", "Category")
    Account = apps.get_model("haushaltsbuch", "Account")
    defaults = get_defaults()
    for i, cat_name in enumerate(defaults.keys()):
        cat = Category.objects.create(name=cat_name, weight=i + 1)
        for j, acc in enumerate(defaults[cat_name]):
            Account.objects.create(name=acc, weight=j + 1, category=cat)


class Migration(migrations.Migration):

    dependencies = [
        ("haushaltsbuch", "0001_initial"),
    ]

    operations = [migrations.RunPython(add_defaults)]
