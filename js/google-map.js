var latArray = [40.7608, 40.8608];
var longArray = [-111.8910, -111.9910];
var iconLibrary = [null, null];

function initMap() {


  var stopLat = parseInt(document.getElementById("stopLat").value);
  var stopLong = parseInt(document.getElementById("stopLong").value);

  var speedLat = parseInt(document.getElementById("speedLat").value);
  var speedLong = parseInt(document.getElementById("speedLong").value);

  var lightLat = parseInt(document.getElementById("lightLat").value);
  var lightLong = parseInt(document.getElementById("lightLong").value);

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
    iconLibrary.push("/Users/viraajreddi/Desktop/traffix/images/mapIcons/redOctagon.png");

  } else if (document.getElementById("speedLat").value != "") {
    latArray.push(speedLat);
    longArray.push(speedLong);
    iconLibrary.push("/Users/viraajreddi/Desktop/traffix/images/mapIcons/speedLimit.png");

  } else if (document.getElementById("lightLat").value != "") {
    latArray.push(lightLat);
    longArray.push(lightLong);
    iconLibrary.push("/Users/viraajreddi/Desktop/traffix/images/mapIcons/trafficLight.png");
  }


    var givenCenter = {lat: 40.7608, lng: -111.8910};


  //latArray.push(givenLatitude);
  //longArray.push(givenLongitude);


    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 8,
      center: givenCenter
    });

    for (i = 0; i < latArray.length; i++) {
    placeMarker(latArray[i], longArray[i], map, contentString, iconLibrary[i]);
    }

}

//_____________________________________________________________________________________________________________________________________________________________________________________________


function visualizeInit() {


    var stopLat = parseInt(document.getElementById("stopLat").value);
    var stopLong = parseInt(document.getElementById("stopLong").value);

    var speedLat = parseInt(document.getElementById("speedLat").value);
    var speedLong = parseInt(document.getElementById("speedLong").value);

    var lightLat = parseInt(document.getElementById("lightLat").value);
    var lightLong = parseInt(document.getElementById("lightLong").value);

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
    }


      var givenCenter = {lat: 40.7608, lng: -111.8910};


    //latArray.push(givenLatitude);
    //longArray.push(givenLongitude);


      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: givenCenter
      });

      for (i = 0; i < latArray.length; i++) {
      placeMarker(latArray[i], longArray[i], map, contentString, iconLibrary[i]);
      }

}
//_____________________________________________________________________________________________________________________________________________________________________________________________

function placeMarker(givenLat, givenLong, map, givenContent, givenIcon) {

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

}