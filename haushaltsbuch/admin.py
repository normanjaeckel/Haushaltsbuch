from django.contrib import admin

from .models import Account, Booking, Category, Reserve


class BookingAdmin(admin.ModelAdmin):
    readonly_fields = ["date", "payment_party", "banking_text", "reference", "amount"]


class AdminSite(admin.AdminSite):
    site_header = "Haushaltsbuch"
    site_title = "Haushaltsbuch"
    index_title = "Übersicht"


admin_site = AdminSite()
admin_site.register(Account)
admin_site.register(Booking, BookingAdmin)
admin_site.register(Category)
admin_site.register(Reserve)
