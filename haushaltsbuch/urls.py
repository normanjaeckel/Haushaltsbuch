from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .admin import admin_site
from .views import Import, Main, Overview

urlpatterns = [
    path("", Main.as_view()),
    path("overview/", Overview.as_view(), name="overview"),
    path("import/", Import.as_view(), name="import"),
    path("admin/", admin_site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
