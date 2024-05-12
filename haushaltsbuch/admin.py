from django.contrib import admin

from .models import Account, Booking, Category, Reserve


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["list_view_str"]

    def list_view_str(self, obj):
        return f"{obj.name} ({obj.weight}) – {obj.account_set.count()} Konten"


class AccountAdmin(admin.ModelAdmin):
    list_display = ["list_view_str"]

    def list_view_str(self, obj):
        return f"{obj.category}: {obj.name} ({obj.weight})"


class BookingAdmin(admin.ModelAdmin):
    list_display = ["date", "amount", "text", "account"]
    list_editable = ["account"]

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ["date", "payment_party", "banking_text", "reference", "amount"]
        return []


class AdminSite(admin.AdminSite):
    site_header = "Haushaltsbuch"
    site_title = "Haushaltsbuch"
    index_title = "Übersicht"


admin_site = AdminSite()
admin_site.register(Account, AccountAdmin)
admin_site.register(Booking, BookingAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Reserve)
