from django.urls import include, re_path as url
from django.contrib import admin

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^moviedb/", include("MovieDB.urls")),
]
