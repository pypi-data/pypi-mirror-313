from django.contrib import admin
from django.urls import re_path as url
from sample.views import SampleFormView

admin.autodiscover()
urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^$", SampleFormView.as_view()),
]
