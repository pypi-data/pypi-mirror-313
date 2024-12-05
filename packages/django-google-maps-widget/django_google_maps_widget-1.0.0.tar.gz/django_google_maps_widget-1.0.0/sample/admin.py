from django.conf import settings
from django.contrib import admin
from django.forms.widgets import TextInput

from django_google_maps_widget.widgets import GoogleMapsAddressWidget
from django_google_maps_widget.fields import AddressField, GeoLocationField

from sample import models


class SampleModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        AddressField: {"widget": GoogleMapsAddressWidget(attrs={"mapid": settings.GOOGLE_MAPS_MAP_ID})},
        GeoLocationField: {"widget": TextInput(attrs={"readonly": "readonly"})},
    }


admin.site.register(models.SampleModel, SampleModelAdmin)
