from django.contrib import admin

from .models import Account, Booking, Category, Reserve


class AdminSite(admin.AdminSite):
    site_header = "Haushaltsbuch"
    site_title = "Haushaltsbuch"
    index_title = "Übersicht"


admin_site = AdminSite()
admin_site.register(Account)
admin_site.register(Booking)
admin_site.register(Category)
admin_site.register(Reserve)
