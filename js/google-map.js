var presetLatArray = [40.2969, 40.2211];
var presetLongArray = [-111.6946, -112.7444];
var presetIconLibrary = ['./images/mapIcons/redOctagon.png', "./images/mapIcons/speedLimit.png", "./images/mapIcons/trafficLight.png"];

var latArray = [];
var longArray = [];
var iconLibrary = [];

var markersArray = [];

function driverMap() {
  //input geocoding stuff here after finished with other map

}

//_____________________________________________________________________________________________________________________________________________________________________________________________


function visualizeInit() {


    var stopLat = parseInt(document.getElementById("stopLat").value);
    var stopLong = parseInt(document.getElementById("stopLong").value);

    var speedLat = parseInt(document.getElementById("speedLat").value);
    var speedLong = parseInt(document.getElementById("speedLong").value);

    var lightLat = parseInt(document.getElementById("lightLat").value);
    var lightLong = parseInt(document.getElementById("lightLong").value);

    var yieldLat = parseInt(document.getElementById("yieldLat").value);
    var yieldLong = parseInt(document.getElementById("yieldLong").value);


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


      var givenCenter = {lat: 40.7608, lng: -111.8910};


    //latArray.push(givenLatitude);
    //longArray.push(givenLongitude);


      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: givenCenter
      });

      for (i = 0; i < presetLatArray.length; i++) {
      presetMarker(presetLatArray[i], presetLongArray[i], map, contentString, presetIconLibrary[i], i);
      }

      for (i = 0; i < latArray.length; i++) {
      placeMarker(latArray[i], longArray[i], map, "", iconLibrary[i], i);
      }

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