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
var yielding = "./images/mapIcons/yeild.png";

var presetIconLibrary = [traffic, traffic, traffic, traffic, traffic, stop, stop, stop, stop, stop, speed, speed];

var latArray = [];
var longArray = [];
var iconLibrary = [];


var laneLat = [];
var laneLong = [];
var c = [];

var markersArray = [];
var flightPathArray = [];


//_____________________________________________________________________________________________________________________________________________________________________________________________


function visualizeInit() {

  const given_geocoder = new google.maps.Geocoder();
  function geocodeAddress(geocoder, address) {
    geocoder.geocode({ address: address }, (results, status) => {
      if (status === "OK") {

        latArray.push(parseFloat(results[0].geometry.location.lat()));
        longArray.push(parseFloat(results[0].geometry.location.lng()));
        //alert(latArray);
      } else {
        alert(
          "Geocode was not successful for the following reason: " + status
        );
      }
    });
  }

    var stopStreet = document.getElementById("stopStreet").value;
    var stopCity = document.getElementById("stopCity").value;
    var stopState = document.getElementById("stopState").value;
    var stopZIP = document.getElementById("stopZIP").value;
    var stopAddress = stopStreet + ", " + stopCity + ", " + stopState + " " + stopZIP;

    var speedStreet = document.getElementById("speedStreet").value;
    var speedCity = document.getElementById("speedCity").value;
    var speedState = document.getElementById("speedState").value;
    var speedZIP = document.getElementById("speedZIP").value;
    var speedAddress = speedStreet + ", " + speedCity + ", " + speedState + " " + speedZIP;

    var lightStreet = document.getElementById("lightStreet").value;
    var lightCity = document.getElementById("lightCity").value;
    var lightState = document.getElementById("lightState").value;
    var lightZIP = document.getElementById("lightZIP").value;
    var lightAddress = lightStreet + ", " + lightCity + ", " + lightState + " " + lightZIP; 

    var yieldStreet = document.getElementById("yieldStreet").value;
    var yieldCity = document.getElementById("yieldCity").value;
    var yieldState = document.getElementById("yieldState").value;
var yieldZIP = document.getElementById("yieldZIP").value;
var yieldAddress = yieldStreet + ", " + yieldCity + ", " + yieldState + " " + yieldZIP; 


    var stopLat = parseFloat(document.getElementById("stopLat").value);
    var stopLong = parseFloat(document.getElementById("stopLong").value);

    var speedLat = parseFloat(document.getElementById("speedLat").value);
    var speedLong = parseFloat(document.getElementById("speedLong").value);

    var lightLat = parseFloat(document.getElementById("lightLat").value);
    var lightLong = parseFloat(document.getElementById("lightLong").value);

    var yieldLat = parseFloat(document.getElementById("yieldLat").value);
    var yieldLong = parseFloat(document.getElementById("yieldLong").value);

    var laneStartLat = parseFloat(document.getElementById("laneStartLat").value);
    var latStartLong = parseFloat(document.getElementById("latStartLong").value);
    var laneEndLat = parseFloat(document.getElementById("laneEndLat").value);
    var laneEndLong = parseFloat(document.getElementById("laneEndLong").value);


//add all info for the infowindows in these 5 arrays below _____________________________________________________________________________________________________________________________________
    var givenFlow = [];
    var givenSpeed = [];
    var givenDensity = [];
    var givenWait = [];
    var givenTravel = [];


    if (document.getElementById("stopStreet").value != "") {
      geocodeAddress(given_geocoder, stopAddress);
      iconLibrary.push(stop);

    } else if (document.getElementById("speedStreet").value != "") {
      geocodeAddress(given_geocoder, speedAddress);
      iconLibrary.push(speed);

    } else if (document.getElementById("lightStreet").value != "") {
      geocodeAddress(given_geocoder, lightAddress);
      iconLibrary.push(traffic);

    } else if (document.getElementById("yieldStreet").value != "") {
      geocodeAddress(given_geocoder, yieldAddress);
      iconLibrary.push("./images/mapIcons/yeild.png");

    } else if (document.getElementById("laneEndLong").value != '') {

      laneLat.push(laneStartLat);
      laneLong.push(latStartLong);
      laneLat.push(laneEndLat);
      laneLong.push(laneEndLong);

    } else if (document.getElementById("stopLat").value != "") {
      latArray.push(stopLat);
      longArray.push(stopLong);
      iconLibrary.push(stop);

    } else if (document.getElementById("speedLat").value != "") {
      latArray.push(speedLat);
      longArray.push(speedLong);
      iconLibrary.push(speed);
      
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


      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: givenCenter
      });

      for (i = 0; i < presetLatArray.length; i++) {
      presetMarker(presetLatArray[i], presetLongArray[i], map, presetIconLibrary[i], i, givenFlow[i], givenSpeed[i], givenDensity[i], givenWait[i], givenTravel[i]);
      }

      for (i = 0; i < latArray.length; i++) {
      placeMarker(latArray[i], longArray[i], map, iconLibrary[i], i, givenFlow[i], givenSpeed[i], givenDensity[i], givenWait[i], givenTravel[i]);
      }

      for (var i = 0; i < laneLat.length; i+=2 ) {

        placeMarker(laneLat[i], laneLong[i], map, "", i, givenFlow[i], givenSpeed[i], givenDensity[i], givenWait[i], givenTravel[i]);

        const flightPlanCoordinates = [
          {
            lat: laneLat[i],
            lng: laneLong[i]
          },
          {
            lat: laneLat[i+1],
            lng: laneLong[i+1]
          }
        ];


        const flightPath = new google.maps.Polyline({
          path: flightPlanCoordinates,
          geodesic: true,
          strokeColor: "#FF0000",
          strokeOpacity: 1.0,
          strokeWeight: 3.5,
          draggable: true
        });


        flightPath.setMap(map);

        flightPathArray.push(flightPath);

      }

      document.getElementById("stopLat").value = '';
      document.getElementById("stopLong").value = '';
      document.getElementById("speedLat").value = '';
      document.getElementById("speedLong").value = '';
      document.getElementById("lightLat").value = '';
      document.getElementById("lightLong").value = '';
      document.getElementById("yieldLat").value = '';
      document.getElementById("yieldLong").value = '';
      document.getElementById("laneStartLat").value = '';
      document.getElementById("latStartLong").value = '';
      document.getElementById("laneEndLat").value = '';
      document.getElementById("laneEndLong").value = '';

      document.getElementById("stopStreet").value = '';
      document.getElementById("stopCity").value = '';
      document.getElementById("stopState").value = '';
      document.getElementById("stopZIP").value = '';

      document.getElementById("stopStreet").value = '';
      document.getElementById("stopCity").value = '';
      document.getElementById("stopState").value = '';
      document.getElementById("stopZIP").value = '';
      stopAddress = '';

    document.getElementById("speedStreet").value = '';
    document.getElementById("speedCity").value = '';
    document.getElementById("speedState").value = '';
    document.getElementById("speedZIP").value = '';
    speedAddress = '';

    document.getElementById("lightStreet").value = '';
    document.getElementById("lightCity").value = '';
    document.getElementById("lightState").value = '';
    document.getElementById("lightZIP").value = '';
    lightAddress = ''; 

    document.getElementById("yieldStreet").value = '';
    document.getElementById("yieldCity").value = '';
    document.getElementById("yieldState").value = '';
    document.getElementById("yieldZIP").value = '';
    yieldAddress = ''; 

}
//_____________________________________________________________________________________________________________________________________________________________________________________________


function placeMarker(givenLat, givenLong, map, givenIcon, givenInt, givenFlow, givenSpeed, givenDensity, givenWait, givenTravel) {

  if (givenIcon == stop) {
    givenFlow = '-10.2% cpm';
    givenSpeed = '-2.2% mph';
    givenDensity = '4% cpl';
    givenWait = '7.45% min';
    givenTravel= '0.7% min';

  } else if (givenIcon == traffic) {
    givenFlow = '+9.1% cpm';
    givenSpeed = '+3.6% mph';
    givenDensity = '-7.7% cpl';
    givenWait = '-8.0% min';
    givenTravel= '-0.9% min';

  } else if (givenIcon == speed) {
    givenFlow = '+4.5% cpm';
    givenSpeed = '+48.3% mph';
    givenDensity = '+10.6% cpl';
    givenWait = '-1.4% min';
    givenTravel= '-4.8% min';

  } else if (givenIcon == "./images/mapIcons/yeild.png") {
    givenFlow = '-13.4% cpm';
    givenSpeed = '-0.8% mph';
    givenDensity = '+3.2% cpl';
    givenWait = '+52.6% min';
    givenTravel= '+ 0.45% min';

  } else if (givenIcon == "") {
    givenFlow = '42.1% cpm';
    givenSpeed = '21.2% mph';
    givenDensity = '-33.2% cpl';
    givenWait = '2.1% min';
    givenTravel = '-20.6% min';
  }

  var contentString1 = '<div id="content">'+
  '<div id="siteNotice">'+
  '</div>'+
  '<div id="bodyContent">'+
  '<p><b>Change in Rates of Flow: </b>' + givenFlow+ '</p>' +
  '<p><b>Change in Average Speed: </b>'+ givenSpeed + '</p>' +
  '<p><b>Change in Vehicle Density: </b>'+ givenDensity + '</p>' +
  '<p><b>Change in Intersection Wait Times: </b>' + givenWait + '</p>' +
  '<p><b>Change in Average Time of Travel: </b>' + givenTravel + '</p>' +
'</div>' +
  '</div>';

        var infowindow = new google.maps.InfoWindow({
          content: contentString1
        });

        var marker = new google.maps.Marker({
            position: {lat: givenLat, lng: givenLong},
            map: map,
            title: 'MARKINGER',
            icon: givenIcon,
            draggable:true
        });

        marker.addListener('click', function() {
          infowindow.open(map, marker);
        });

        marker.addListener('rightclick', function(event) {
        marker.setMap(null);
        });

        marker.addListener('dragend', function(evt) {
          var position = marker.getPosition()
          var dragLat = position.lat()
          var dragLong = position.lng()

          latArray[givenInt] = dragLat;
          longArray[givenInt] = dragLong;
        });

markersArray.push(marker);

}

function presetMarker(givenLat, givenLong, map, givenIcon, givenInt, givenFlow, givenSpeed, givenDensity, givenWait, givenTravel) {

  var contentString1 = '<div id="content">'+
  '<div id="siteNotice">'+
  '</div>'+
  '<div id="bodyContent">'+
  '<p><b>Change in Rates of Flow: </b>' + givenFlow+ '</p>' +
  '<p><b>Change in Average Speed: </b>'+ givenSpeed + '</p>' +
  '<p><b>Change in Vehicle Density: </b>'+ givenDensity + '</p>' +
  '<p><b>Change in Intersection Wait Times: </b>' + givenWait + '</p>' +
  '<p><b>Change in Average Time of Travel: </b>' + givenTravel+ '</p>'
'</div>'+
  '</div>';

  var contentString2 = '<div id="content">'+
  '<div id="siteNotice">'+
  '</div>'+
  '<div id="bodyContent">'+
  '<p><b>Change in Rates of Flow: </b>' + '+8.7% cpm' + '</p>' +
  '<p><b>Change in Average Speed: </b>'+ '+1.5% mph' + '</p>' +
  '<p><b>Change in Vehicle Density: </b>'+ '-9.3% cpl' + '</p>' +
  '<p><b>Change in Intersection Wait Times: </b>' + '-8.4% min' + '</p>' +
  '<p><b>Change in Average Time of Travel: </b>' + '-1.2% min' + '</p>'
'</div>'+
  '</div>';

  var contentString3 = '<div id="content">'+
  '<div id="siteNotice">'+
  '</div>'+
  '<div id="bodyContent">'+
  '<p><b>Change in Rates of Flow: </b>' + '-12.1% cpm' + '</p>' +
  '<p><b>Change in Average Speed: </b>'+ '-0.64% mph' + '</p>' +
  '<p><b>Change in Vehicle Density: </b>'+ '+3.1% cpl' + '</p>' +
  '<p><b>Change in Intersection Wait Times: </b>' + '+51.4% min' + '</p>' +
  '<p><b>Change in Average Time of Travel: </b>' + '+0.59% min' + '</p>'
'</div>'+
  '</div>';

  var contentString4 = '<div id="content">'+
  '<div id="siteNotice">'+
  '</div>'+
  '<div id="bodyContent">'+
  '<p><b>Change in Rates of Flow: </b>' + '-8.7% cpm' + '</p>' +
  '<p><b>Change in Average Speed: </b>'+ '-1.6% mph' + '</p>' +
  '<p><b>Change in Vehicle Density: </b>'+ '+5.8% cpl' + '</p>' +
  '<p><b>Change in Intersection Wait Times: </b>' + '+8.22% min' + '</p>' +
  '<p><b>Change in Average Time of Travel: </b>' + '+1.3% min' + '</p>'
'</div>'+
  '</div>';


        var infowindow = new google.maps.InfoWindow({
          content: contentString1
        });

        var marker = new google.maps.Marker({
            position: {lat: givenLat, lng: givenLong},
            map: map,
            title: 'MAPPETH',
            icon: givenIcon,
            draggable:false
        });

        marker.addListener('click', function() {
          infowindow.open(map, marker);
        });

        marker.addListener('rightclick', function() {

          if (givenIcon == './images/mapIcons/redOctagon.png') {

            infowindow.setContent(contentString2);
            marker.setIcon("./images/mapIcons/yeild.png");
            givenIcon = "./images/mapIcons/yeild.png";



          } else if (givenIcon == "./images/mapIcons/yeild.png") {

            infowindow.setContent(contentString3);
            marker.setIcon("./images/mapIcons/trafficLight.png");
            givenIcon = "./images/mapIcons/trafficLight.png";

          } else if (givenIcon == "./images/mapIcons/trafficLight.png") {

            infowindow.setContent(contentString4);
            marker.setIcon("./images/mapIcons/redOctagon.png");
            givenIcon = "./images/mapIcons/redOctagon.png";
          }



          });

}

function deleteMarkers() {

  for (var i = 0; i < markersArray.length; i++ ) {
    markersArray[i].setMap(null);
  }

  for (var i = 0; i < flightPathArray.length; i++ ) {
    flightPathArray[i].setMap(null);
  }

  markersArray.length = 0;
  flightPathArray.length = 0;
}
