var presetLatArray = [
  33.771277,
  33.763901,
  33.763963,
  33.767460,
  33.767527,
  33.767798,
  33.768723,
  33.768654,
  33.768404,
  33.764832,
  33.766621,
  33.768580
];

var presetLongArray = [
  -84.374786,
  -84.367821,
  -84.371933,
  -84.378112,
  -84.382028,
  -84.371164,
  -84.381070,
  -84.381943,
  -84.371846,
  -84.370435,
  -84.371927,
  -84.377872
];

var stop = './images/mapIcons/redOctagon.png';
var speed = "./images/mapIcons/speedLimit.png";
var traffic = "./images/mapIcons/trafficLight.png";

var presetIconLibrary = [traffic, traffic, traffic, traffic, traffic, stop, stop, stop, stop, stop, speed, speed];

var latArray = [];
var longArray = [];
var iconLibrary = [];

var markersArray = [];

function driverMap() {
  //input geocoding stuff here after finished with other map

}

//_____________________________________________________________________________________________________________________________________________________________________________________________


function visualizeInit() {


    var stopLat = parseFloat(document.getElementById("stopLat").value);
    var stopLong = parseFloat(document.getElementById("stopLong").value);

    var speedLat = parseFloat(document.getElementById("speedLat").value);
    var speedLong = parseFloat(document.getElementById("speedLong").value);

    var lightLat = parseFloat(document.getElementById("lightLat").value);
    var lightLong = parseFloat(document.getElementById("lightLong").value);

    var yieldLat = parseFloat(document.getElementById("yieldLat").value);
    var yieldLong = parseFloat(document.getElementById("yieldLong").value);


    /*
    var weather = document.getElementById("forcedWeather").value;
    var speedLimit = document.getElementById("forcedSpeed").value;
    var roadSigns = document.getElementById("roadSignsS").value;
    var roadShape = document.getElementById("roadShapes").value;*/




    var contentString = '<div id="content">'+
                '<div id="siteNotice">'+
                '</div>'+
                '<div id="bodyContent">'+
                '</div>';

    if (document.getElementById("stopLat").value != "") {
      latArray.push(stopLat);
      longArray.push(stopLong);
      iconLibrary.push("./images/mapIcons/redOctagon.png");

    } else if (document.getElementById("speedLat").value != "") {
      latArray.push(speedLat);
      longArray.push(speedLong);
      iconLibrary.push("./images/mapIcons/speedLimit.png");

    } else if (document.getElementById("lightLat").value != "") {
      latArray.push(lightLat);
      longArray.push(lightLong);
      iconLibrary.push("./images/mapIcons/trafficLight.png");
    } else if (document.getElementById("yieldLat").value != "") {
      latArray.push(yieldLat);
      longArray.push(yieldLong);
      iconLibrary.push("./images/mapIcons/yeild.png");
    }


      var givenCenter = {lat: 33.767596, lng: -84.374892};


    //latArray.push(givenLatitude);
    //longArray.push(givenLongitude);


      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: givenCenter
      });

      for (i = 0; i < presetLatArray.length; i++) {
      presetMarker(presetLatArray[i], presetLongArray[i], map, contentString, presetIconLibrary[i], i);
      }

      for (i = 0; i < latArray.length; i++) {
      placeMarker(latArray[i], longArray[i], map, "", iconLibrary[i], i);
      }


      document.getElementById('stopLat').value = '';
      document.getElementById('stopLong').value = '';
      document.getElementById('speedLat').value = '';
      document.getElementById('speedLong').value = '';
      document.getElementById('lightLat').value = '';
      document.getElementById('lightLong').value = '';
      document.getElementById('yieldLat').value = '';
      document.getElementById('yieldLong').value = '';

}
//_____________________________________________________________________________________________________________________________________________________________________________________________

function placeMarker(givenLat, givenLong, map, givenContent, givenIcon, givenInt) {

        var infowindow = new google.maps.InfoWindow({
          content: givenContent
        });

        var marker = new google.maps.Marker({
            position: {lat: givenLat, lng: givenLong},
            map: map,
            title: 'GIVEEEEN MEEEAAAPP',
            icon: givenIcon,
            draggable:true
        });

        marker.addListener('click', function() {
          infowindow.open(map, marker);
        });

        marker.addListener('rightclick', function(event) {
        marker.setMap(null);
        });


markersArray.push(marker);

}

function presetMarker(givenLat, givenLong, map, givenContent, givenIcon, givenInt) {

        var infowindow = new google.maps.InfoWindow({
          content: givenContent
        });

        var marker = new google.maps.Marker({
            position: {lat: givenLat, lng: givenLong},
            map: map,
            title: 'GIVEEEEN MEEEAAAPP',
            icon: givenIcon,
            draggable:false
        });

        marker.addListener('click', function() {
          if (givenIcon == './images/mapIcons/redOctagon.png') {

            marker.setIcon("./images/mapIcons/yeild.png");
            givenIcon = "./images/mapIcons/yeild.png";

          } else if (givenIcon == "./images/mapIcons/yeild.png") {

            marker.setIcon("./images/mapIcons/trafficLight.png");
            givenIcon = "./images/mapIcons/trafficLight.png";

          } else if (givenIcon == "./images/mapIcons/trafficLight.png") {

            marker.setIcon("./images/mapIcons/redOctagon.png");
            givenIcon = "./images/mapIcons/redOctagon.png";
          }

        });

}

function deleteMarkers() {

  for (var i = 0; i < markersArray.length; i++ ) {

    markersArray[i].setMap(null);

  }

  markersArray.length = 0;

}
