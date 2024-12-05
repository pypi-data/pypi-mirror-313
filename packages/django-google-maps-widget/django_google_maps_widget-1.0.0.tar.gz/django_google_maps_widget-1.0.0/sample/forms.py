from django import forms
from django.conf import settings
from sample.models import SampleModel
from django_google_maps_widget.widgets import GoogleMapsAddressWidget


class SampleForm(forms.ModelForm):
    class Meta(object):
        model = SampleModel
        fields = ["address", "geolocation"]
        widgets = {
            "address": GoogleMapsAddressWidget(attrs={"mapid": settings.GOOGLE_MAPS_MAP_ID}),
        }
