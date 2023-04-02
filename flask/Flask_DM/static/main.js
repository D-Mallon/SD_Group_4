console.log("Bike data:", bikeData); // Add this line

function initMap() {
    const dublin = { lat: 53.349805, lng: -6.26031 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: dublin,
    });

    bikeData.forEach((station) => {
    const marker = new google.maps.Marker({
        position: { lat: station.latitude, lng: station.longitude },
        map: map,
        title: station.name,
    });

    const infoWindow = new google.maps.InfoWindow({
        content: `<div>
                    <h3>${station.name}</h3>
                    <p>Station Number: ${station.number}</p>
                    <p>Available Bikes: ${station.available_bikes}</p>
                    <p>Capacity: ${station.capacity}</p>
                  </div>`
    });

    marker.addListener("click", () => {
        infoWindow.open(map, marker);
    });
});
}

// code was kind of working with the below included. Can probably drop this as its removal got rid of a few errors
// $(document).ready(function () {
//     initMap();
// });
