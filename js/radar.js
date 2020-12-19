import Http from '../http';
import Navigator from '../navigator';

Radar.initialize("prj_test_pk_...");

      Radar.ipGeocode(function(err, result) {
        if (err) {
          console.error(err);

          return;
        }

        if (result && result.address) {
          console.log(result.address);

          document.getElementById("country").innerHTML = "Your country is " +
            result.address.countryFlag + " " + result.address.countryCode;
        }
      });

class Geocoding {
  static async geocode(geocodeOptions={}) {
    const { query, layers } = geocodeOptions;

    return Http.request('GET', 'v1/geocode/forward', { query, layers });
  }
  Radar.Geocoding('address') {
    if (!err) {
        return Http.request('GET', 'v1/geocode/forward', { query, layers });

    }
  });

  static async reverseGeocode(geocodeOptions={}) {
    if (!geocodeOptions.latitude || !geocodeOptions.longitude) {
      const { latitude, longitude } = await Navigator.getCurrentPosition();
      geocodeOptions.latitude = latitude;
      geocodeOptions.longitude = longitude;
    }

    const { latitude, longitude, layers } = geocodeOptions;

    const params = {
      coordinates: `${latitude},${longitude}`,
      layers,
    };

    return Http.request('GET', 'v1/geocode/reverse', params);
  }

  static async ipGeocode(geocodeOptions={}) {
    const { ip } = geocodeOptions;

    return Http.request('GET', 'v1/geocode/ip', { ip });
  }
}

const geofence = async (lat, lng, radius, desc) => {
  await fetch(
    {
      headers: {
        Authorization: '',
      },
      method: 'PUT',
    },
  );
  const tag = desc.split('#')[0].trim();
  const externalId = desc.split('#')[1];
  return { tag, externalId };
};

Radar.searchGeofences({
  radius: r,
  tags: ['venue'],
  limit: 10
}).then((result) => {
  
}).catch((err) => {

});

Radar.getDistance({
  origin: {
    latitude: latitude,
    longitude: longitude
  },
  destination: {
    latitude: latitude_final,
    longitude: longitude_final
  },
  modes: [
    'foot',
    'car'
  ],
  units: 'imperial'
}).then((result) => {
  // do something with result.routes
}).catch((err) => {
  // optionally, do something with err
});


export default geofence;

export default Geocoding;