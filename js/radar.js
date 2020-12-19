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
    `https://api.radar.io/v1/geofences?description=${desc}&type=circle&coordinates=[${lng},${lat}]&radius=${radius}`,
    {
      headers: {
        Authorization: 'prj_live_pk_9960fa9015ec1c672178a43fa62142afc16b6aed',
      },
      method: 'PUT',
    },
  );
  const tag = desc.split('#')[0].trim();
  const externalId = desc.split('#')[1];
  return { tag, externalId };
};

export default geofence;

export default Geocoding;