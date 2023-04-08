// initMap is supposed to create a new google maps object AND is supposed to add markers for each location from the PLACEHOLDER_DATA by using a for loop.
function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 53.3498, lng: -6.2603 },
    zoom: 13,
  });

  const infoWindow = new google.maps.InfoWindow();

  for (const [title, lat, lng] of PLACEHOLDER_DATA) {
    const marker = new google.maps.Marker({
      position: { lat, lng },
      map,
      title,
    });

    // when marker clicked, this is supposed to pop an info window up.
    marker.addListener("click", () => {
      infoWindow.close();
      infoWindow.setContent(marker.title);
      infoWindow.open(marker.map, marker);
    });
  }
}

//this is supposed to create a new script element and append it to the HTML document's body element to load the Google Maps JavaScript API asynchronously.
// Add this event listener
window.addEventListener('load', () => {
  const script = document.createElement('script');
  script.src = 'https://maps.googleapis.com/maps/api/js?key=API_KEY_HERE&callback=initMap';
  script.async = true;
  script.defer = true;
  document.body.appendChild(script);
});
