let bikeData;
let todayChart;
let yesterdayChart;
let dayBeforeYesterdayChart;
let averageTodayChart;
let shouldCloseCharts = false; //including this flag to ensure charts close as during testing, quickly moving between windows and closing windows wasn't acknowledged.



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
        const percentageAvailable = (station.available_bikes / station.capacity) * 100;

        let markerColor;
        if (percentageAvailable <= 10) {
            markerColor = "red";
        } else if (percentageAvailable >= 10.1 && percentageAvailable <= 75) {
            markerColor = "blue";
        } else {
            markerColor = "green";
        }

        const marker = new google.maps.Marker({
            position: { lat: station.latitude, lng: station.longitude },
            map: map,
            draggable: true,
            animation: google.maps.Animation.DROP,
            title: station.name,
            icon: {
                url: `http://maps.google.com/mapfiles/ms/icons/${markerColor}-dot.png`,
            },
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

        function closeAverageChart() {
            document.getElementById('average-chart-container').style.display = 'none';
        }

        // Adding the event listener for when the info window is closed, which hides the charts
        infoWindow.addListener("closeclick", () => {
            shouldCloseCharts = true; // testing situation where multiple info windows selected quickly and last close window actioned
            closeCharts();
            closeAverageChart();
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

                // This calls onMarkerClick when a marker is clicked
                onMarkerClick(station.number);
                 // Shows the new chart when a marker is clicked
                document.getElementById('average-chart-container').style.display = 'block';
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


async function onMarkerClick(stationNumber) {
    shouldCloseCharts = false;
    try {
        const response = await fetch(`/station_data/${stationNumber}`);
        const data = await response.json();

        if (shouldCloseCharts) {
            closeCharts();
            closeAverageChart();
            return;
        }

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

        // Fetch the average station data
        const avgResponse = await fetch(`/average_station_data/${stationNumber}`);
        const avgData = await avgResponse.json();

        if (shouldCloseCharts) {
            closeCharts();
            closeAverageChart();
            return;
        }

        // Update the average hourly availability chart
        averageTodayChart.data.labels = avgData.labels;
        averageTodayChart.data.datasets[0].data = avgData.data;
        averageTodayChart.update();

    } catch (error) {
        console.error("Error fetching station data:", error);
    }
}


function getDayName(offset) {
    const today = new Date();
    const targetDate = new Date(today.setDate(today.getDate() - offset));
    const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

    return weekdays[targetDate.getDay()];
}

function initCharts() {
    const chartOptions = (title) => {
        return {
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
                plugins: {
                    title: {
                        display: true,
                        text: title,
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        };
    };

    todayChart = new Chart(document.getElementById('todayChart'), chartOptions("Today's average hourly availability"));
    yesterdayChart = new Chart(document.getElementById('yesterdayChart'), chartOptions(`${getDayName(1)}'s average hourly availability`));
    dayBeforeYesterdayChart = new Chart(document.getElementById('dayBeforeYesterdayChart'), chartOptions(`${getDayName(2)}'s average hourly availability`));
    averageTodayChart = new Chart(document.getElementById('averageTodayChart'), chartOptions("Today's average hourly availability (all-time)"));
}


fetchData().then(() => {
    initMap();
    initCharts();
});