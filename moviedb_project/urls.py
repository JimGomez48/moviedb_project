from django.contrib import admin
from django.urls import include
from django.urls import re_path as url

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^MovieDB/", include("MovieDB.urls")),
]
