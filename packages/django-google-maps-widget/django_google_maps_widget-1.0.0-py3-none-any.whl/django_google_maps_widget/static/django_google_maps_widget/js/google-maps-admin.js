
/*
Integration for Google Maps in the django admin.

How it works:

You have an address field on the page.
Enter an address and an on change event will update the map
with the address. A marker will be placed at the address.
If the user needs to move the marker, they can and the geolocation
field will be updated.

Only one marker will remain present on the map at a time.

This script expects:

<input type="text" name="address" id="id_address" />
<input type="text" name="geolocation" id="id_geolocation" />

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

*/


let autocomplete;
let geocoder;
let map;
let marker;

const geolocationId = 'id_geolocation';
const addressId = 'id_address';
const mapHostId = 'map_canvas';

async function initialize() {
    const { Map } = await google.maps.importLibrary("maps");
    const { Autocomplete } = await google.maps.importLibrary("places");
    const { Geocoder } = await google.maps.importLibrary("geocoding");
    geocoder = new Geocoder();

    let lat = 0;
    let lng = 0;
    let zoom = 2;
    // set up initial map to be world view. also, add change
    // event so changing address will update the map
    let existinglocation = getExistingLocation();

    if (existinglocation) {
        lat = existinglocation[0];
        lng = existinglocation[1];
        zoom = 18;
    }

    let latlng = new google.maps.LatLng(lat, lng);
    let myOptions = {
        zoom: zoom,
        center: latlng,
        mapTypeId: getMapType()
    };
    const addressField = document.getElementById(addressId);
    const mapHost = document.getElementById(mapHostId);

    if (addressField.hasAttribute("mapid")) {
        myOptions.mapId = addressField.getAttribute("mapid")
    }

    map = new Map(mapHost, myOptions);
    if (existinglocation) {
        setMarker(latlng);
    }


    autocomplete = new Autocomplete(
                /** @type {!HTMLInputElement} */(addressField),
        getAutoCompleteOptions());

    // this only triggers on enter, or if a suggested location is chosen
    // todo: if a user doesn't choose a suggestion and presses tab, the map doesn't update
    autocomplete.addListener("place_changed", codeAddress);

    // don't make enter submit the form, let it just trigger the place_changed event
    // which triggers the map update & geocode
    addressField.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            return false;
        }
    });
}

function getMapType() {
    // https://developers.google.com/maps/documentation/javascript/maptypes
    const geolocation = document.getElementById(addressId);
    const allowedType = ['roadmap', 'satellite', 'hybrid', 'terrain'];
    const mapType = geolocation.getAttribute('data-map-type');

    if (mapType && -1 !== allowedType.indexOf(mapType)) {
        return mapType;
    }

    return google.maps.MapTypeId.HYBRID;
}

function getAutoCompleteOptions() {
    const geolocation = document.getElementById(addressId);
    const autocompleteOptions = geolocation.getAttribute('data-autocomplete-options');

    if (!autocompleteOptions) {
        return {
            types: ['geocode']
        };
    }

    return JSON.parse(autocompleteOptions);
}

function getExistingLocation() {
    let geolocation = document.getElementById(geolocationId).value;
    if (geolocation) {
        return geolocation.split(',');
    }
}

function codeAddress() {
    let place = autocomplete.getPlace();

    if (place.geometry !== undefined) {
        updateWithCoordinates(place.geometry.location);
    }
    else {
        geocoder.geocode({ 'address': place.name }, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var latlng = results[0].geometry.location;
                self.updateWithCoordinates(latlng);
            } else {
                alert("Geocode was not successful for the following reason: " + status);
            }
        });
    }
}

function updateWithCoordinates(latlng) {
    map.setCenter(latlng);
    map.setZoom(18);
    setMarker(latlng);
    updateGeolocation(latlng);
}

function setMarker(latlng) {
    if (marker) {
        updateMarker(latlng);
    } else {
        addMarker({ 'latlng': latlng, 'draggable': true });
    }
}

async function addMarker(Options) {
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
    let draggable = Options.draggable || false;
    marker = new AdvancedMarkerElement({
        map: map,
        position: Options.latlng,
        gmpDraggable: draggable,
    });

    if (draggable) {
        addMarkerDrag();
    }
}

function addMarkerDrag() {
    marker.addListener('dragend', (event) => {
        updateGeolocation(event.latLng);
    });
}

function updateMarker(latlng) {
    marker.setPosition(latlng);
}

function updateGeolocation(latlng) {
    const geolocationField = document.getElementById(geolocationId);
    geolocationField.value = latlng.lat() + "," + latlng.lng();
    const event = new Event('change');
    geolocationField.dispatchEvent(event);
}

initialize();
