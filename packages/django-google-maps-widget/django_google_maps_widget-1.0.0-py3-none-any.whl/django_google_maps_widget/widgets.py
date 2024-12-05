from django.conf import settings
from django.templatetags.static import static
from django.forms import widgets
from django.utils.html import html_safe


@html_safe
class MapsAdminScript:
    def __str__(self) -> str:
        return f'<script src="{static("django_google_maps_widget/js/google-maps-admin.js")}" type="module"></script>'


class GoogleMapsAddressWidget(widgets.TextInput):
    """a widget that will place a google map right after the #id_address field"""

    template_name = "django_google_maps_widget/widgets/map_widget.html"

    class Media:
        css = {"all": ("django_google_maps_widget/css/google-maps-admin.css",)}
        js = (
            (
                f"https://maps.googleapis.com/maps/api/js"
                f"?key={settings.GOOGLE_MAPS_API_KEY}&libraries=maps,marker,places,geocoding"
            ),
            MapsAdminScript(),
        )
