// console.log("Bike data:", bikeData); // Add this line

function initMap() {
    const dublin = { lat: 53.349805, lng: -6.26031 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: dublin,
    });

    let activeInfoWindow; // Keep track of the currently open info window
    let activeMarker; // Keep track of the currently active marker

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
            if (activeInfoWindow && activeMarker === marker) {
                activeInfoWindow.close();
                activeInfoWindow = null;
                activeMarker = null;
            } else {
                if (activeInfoWindow) {
                    activeInfoWindow.close();
                }
                infoWindow.open(map, marker);
                activeInfoWindow = infoWindow;
                activeMarker = marker;
            }
        });
    });
}


