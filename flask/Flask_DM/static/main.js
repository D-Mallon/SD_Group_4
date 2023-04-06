let bikeData;
let todayChart;
let yesterdayChart;
let dayBeforeYesterdayChart;


//initializes a Google Map and creates markers for each bike station using the data obtained from the server
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
            draggable: true,
            animation: google.maps.Animation.DROP,
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

        function closeCharts() {
            document.getElementById('chart-container').style.display = 'none';
        }

        // Adding the event listener for when the info window is closed, which hides the charts
        infoWindow.addListener("closeclick", () => {
            closeCharts();
        });

        marker.addListener("click", () => {
            if (activeInfoWindow && activeMarker === marker) {
                activeInfoWindow.close();
                activeInfoWindow = null;
                activeMarker = null;
                closeCharts(); // Closes the charts when the info window from marker is closed
            } else {
                if (activeInfoWindow) {
                    activeInfoWindow.close();
                }
                infoWindow.open(map, marker);
                activeInfoWindow = infoWindow;
                activeMarker = marker;

                // Add this line to call onMarkerClick when a marker is clicked
                onMarkerClick(station.number);
            }
        });
    });
}


async function fetchData() {
    try {
        const response = await fetch("/bike_stations");
        bikeData = await response.json();
        initMap();
    } catch (error) {
        console.error("Error fetching bike data:", error);
    }
}

fetchData();

async function onMarkerClick(stationNumber) {
    try {
        const response = await fetch(`/station_data/${stationNumber}`);
        const data = await response.json();

        document.getElementById('chart-container').style.display = 'block';

        // Update today chart
        todayChart.data.labels = data.today.labels;
        todayChart.data.datasets[0].data = data.today.data;
        todayChart.update();

        // Update yesterday chart
        yesterdayChart.data.labels = data.yesterday.labels;
        yesterdayChart.data.datasets[0].data = data.yesterday.data;
        yesterdayChart.update();

        // Update day before yesterday chart
        dayBeforeYesterdayChart.data.labels = data.dayBeforeYesterday.labels;
        dayBeforeYesterdayChart.data.datasets[0].data = data.dayBeforeYesterday.data;
        dayBeforeYesterdayChart.update();
    } catch (error) {
        console.error("Error fetching station data:", error);
    }
}


function initCharts() {
    const chartOptions = {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Available Bikes',
                    data: [],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    };

    todayChart = new Chart(document.getElementById('todayChart'), chartOptions);
    yesterdayChart = new Chart(document.getElementById('yesterdayChart'), chartOptions);
    dayBeforeYesterdayChart = new Chart(document.getElementById('dayBeforeYesterdayChart'), chartOptions);
}

fetchData().then(() => {
    initMap();
    initCharts();
});
