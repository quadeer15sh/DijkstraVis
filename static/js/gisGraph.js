var map = L.map(
    "map",
    {
        center: [19.10535888255391, 73.00904315536212],
        crs: L.CRS.EPSG3857,
        zoom: 16,
        zoomControl: true,
        preferCanvas: false,
    }
);

var latlngs = [];
var markers = [];
var i = 0;
var counter = 0;
var gis_info = {};
var edge_info = [];
var graph_info = {};
var src_dest = [];

var icon_src = L.AwesomeMarkers.icon(
    {"extraClasses": "fa-rotate-0",  "markerColor": "green", "prefix": "glyphicon"}
);

var icon_dest = L.AwesomeMarkers.icon(
    {"extraClasses": "fa-rotate-0",  "markerColor": "red", "prefix": "glyphicon"}
);

function deg2rad(deg) {
    return deg * (Math.PI / 180);
}

function getDistance(lat1, lon1, lat2, lon2) {
    var R = 6371; // Radius of the earth in km
    var dLat = this.deg2rad(lat2 - lat1);  // deg2rad below
    var dLon = this.deg2rad(lon2 - lon1);
    var a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2)
        ;
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var d = R * c; // Distance in km
    return d;
}

function onMapClick(e) {
    console.log("You clicked the map at " + e.latlng);
    var geo = e.latlng;
    var marker = L.marker([e.latlng.lat, e.latlng.lng]).addTo(map);
    console.log("Prev ID: "+e.target._leaflet_id);
    counter++;
    
    marker.on('click', function (e) {
        marker.bindPopup('Vertex: ' + e.target._leaflet_id + '<br>');
        marker.addTo(map);
    });

    marker.on('click',function(event){
        console.log("Key press done succesfully");
        if (src_dest.length < 2) {
            var r = confirm("Are you sure you want this to be the source node ?");
            src_dest.push(event.target._leaflet_id);
            if ( src_dest.length == 1) {
                event.target.setIcon(icon_src);    
            } else {
                event.target.setIcon(icon_dest);
            }
        }
    });

    marker.on('dblclick', function (e) {
        if (src_dest.length < 2){
            alert("Please select the source and destination");
            return;
        }
        latlngs.push([e.latlng.lat, e.latlng.lng]);
        gis_info[e.target._leaflet_id] = [e.latlng.lat, e.latlng.lng];
        console.log("ID: "+e.target._leaflet_id);
        markers.push(e.target._leaflet_id);
        
        if (latlngs.length == 2) {
            var weight = getDistance(latlngs[0][0], latlngs[0][1], latlngs[1][0], latlngs[1][1]);
            var info = {'edge':markers,'weight':weight};
            edge_info.push(info);
            edges = {'vertices':counter,'edges':edge_info,'geocodes':gis_info,'src_dest':src_dest};
            console.log("Edge Info"+JSON.stringify(edges));
            var polyline = L.polyline(latlngs, { color: 'red' }).addTo(map);
            latlngs = [];
            markers = [];
        }
    });
}

map.on('dblclick', onMapClick);

var sendRequest = function()
{
    if(src_dest.length == 2){
        console.log("Button was clicked");
    $.ajax({
        type: 'POST',
       contentType: 'application/json',
       data: JSON.stringify(edges),
       dataType: 'json',
       url: '/index',
       success: function (e) {
           window.location = "/display";
           console.log("Request sent successfully");
           console.log(e);
           console.log(e['distance']);
           document.getElementById('distance').innerHTML = e['distance'];
       },
       error: function(error) {
       console.log(error);
       console.log("There was an error");
   }
   });
    }
    else{
        alert("Please select the source and destination");
    }
}
document.getElementById('path').onclick = sendRequest;

var tile_layer = L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    { "attribution": "Data by \u0026copy; \u003ca href=\"http://openstreetmap.org\"\u003eOpenStreetMap\u003c/a\u003e, under \u003ca href=\"http://www.openstreetmap.org/copyright\"\u003eODbL\u003c/a\u003e.", "detectRetina": false, "maxNativeZoom": 18, "maxZoom": 18, "minZoom": 0, "noWrap": false, "opacity": 1, "subdomains": "abc", "tms": false }
).addTo(map);

// You clicked the map at LatLng(19.105225, 73.009193) destination
// You clicked the map at LatLng(19.106061, 73.008925)
// You clicked the map at LatLng(19.102921, 72.997725)
// You clicked the map at LatLng(19.097746, 72.999272) source
// You clicked the map at LatLng(19.10094, 73.010547)
