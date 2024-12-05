=========================
django-google-maps-widget
=========================

|Build Status|

``django-google-maps-widget`` is a simple library that provides the basic
hooks into `Google Maps Platform`_ for use in Django models from Django
version 4.2+. Supports Python 3.9+. Forked from `this project`_ originally authored by `@madisona`_, with adaptation to the modern Python environment.

This library is useful to allow someone from the admin panels to type a freeform
address, have the address geocoded on change and plotted on the map. If
the location is not 100% correct, the user can drag the marker to the
correct spot and the geo coordinates will update.

Usage
------

-  Include the ``django_google_maps_widget`` app in your ``settings.py``

-  Add your Google Maps API Key in your ``settings.py`` as
   ``GOOGLE_MAPS_API_KEY``

-  Add your Google Maps map ID in your ``settings.py`` as
   ``GOOGLE_MAPS_MAP_ID`` (recommended). Map ID is necessary for the map
   to function and is injected via field attribute, but you can provide
   this attribute however you want.

-  Create a model that has both an address field and geolocation field:

   .. code:: python

      from django.db import models
      from django_google_maps_widget import fields as map_fields

      class Rental(models.Model):
          address = map_fields.AddressField(max_length=200)
          geolocation = map_fields.GeoLocationField(max_length=100)

-  In the ``admin.py``, include the following as a ``formfield_override``:

   .. code:: python

      from django.contrib import admin
      from django_google_maps_widget import widgets as map_widgets
      from django_google_maps_widget import fields as map_fields

      class RentalAdmin(admin.ModelAdmin):
          formfield_overrides = {
              map_fields.AddressField: {
               "widget": map_widgets.GoogleMapsAddressWidget(attrs={
                  "mapid": settings.GOOGLE_MAPS_MAP_ID
               })
             },
          }

-  To change the map type (``hybrid`` by default), you can add an html
   attribute on the ``AddressField`` widget. The list of allowed values
   is: ``hybrid``, ``roadmap``, ``satellite``, ``terrain``

   .. code:: python

      from django.contrib import admin
      from django_google_maps_widget import widgets as map_widgets
      from django_google_maps_widget import fields as map_fields

      class RentalAdmin(admin.ModelAdmin):
          formfield_overrides = {
              map_fields.AddressField: {
                "widget": map_widgets.GoogleMapsAddressWidget(attrs={"data-map-type": "roadmap"})},
          }

-  To change the autocomplete options, you can add an html attribute on
   the ``AddressField`` widget. See
   https://developers.google.com/maps/documentation/javascript/places-autocomplete#add_autocomplete
   for a list of available options

   .. code:: python

      import json from django.contrib import admin
      from django_google_maps_widget import widgets as map_widgets
      from django_google_maps_widget import fields as map_fields

      class RentalAdmin(admin.ModelAdmin): formfield_overrides = {
          map_fields.AddressField: { "widget":
          map_widgets.GoogleMapsAddressWidget(attrs={
            "data-autocomplete-options": json.dumps({ "types": ["geocode",
            "establishment"], "componentRestrictions": {
                        "country": "us"
                    }
                })
            })
          },
      }

That should be all you need to get started.

It can be useful to make the geolocation field readonly in the admin so a user
doesn't accidentally change it to a nonsensical value. There is
validation on the field, so you can't enter an incorrect value, but you could
enter something that is not even close to the address you intended.

When you're displaying the address back to the user, just request the map
using the geocoordinates that were saved in your model.

.. |Build Status| image:: https://github.com/amv-bamboo/django-google-maps/actions/workflows/django.yml/badge.svg
   :target: https://github.com/amv-bamboo/django-google-maps/actions/workflows/django.yml
.. _Google Maps Platform: https://developers.google.com/maps/documentation/javascript/overview
.. _this project: https://github.com/madisona/django-google-maps/
.. _@madisona: https://github.com/madisona/
