let bikeData;
let todayChart;
let yesterdayChart;
let dayBeforeYesterdayChart;
let averageTodayChart;
let userloc;
let destloc;
let directionsService;
let directionsRenderer;
let map;
let shouldCloseCharts = false

//initializes a Google Map and creates markers for each bike station using the data obtained from the server
function initMap() {
    const dublin = { lat: 53.349805, lng: -6.26031 };
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: dublin,
    });

    directionsService = new google.maps.DirectionsService,
    directionsRenderer = new google.maps.DirectionsRenderer({
            map: map
                    }),
   
    

    autocompleteStart = new google.maps.places.Autocomplete(document.getElementById('autocompleteStart'),
    {
        types:['establishment'],
        componentRestrictions:{'country':['IE']},
        fields:['place_id','geometry','name']
    });

    autocompleteEnd = new google.maps.places.Autocomplete(document.getElementById('autocompleteEnd'),
    {
        types:['establishment'],
        componentRestrictions:{'country':['IE']},
        fields:['place_id','geometry','name']
    });

    autocompleteStart.addListener ('place_changed', onPlaceChangedStart);
    autocompleteEnd.addListener ('place_changed', onPlaceChangedEnd);

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
            draggable: false,
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

                // This calls onMarkerClick when a marker is clicked
                onMarkerClick(station.number);
                 // Shows the new chart when a marker is clicked
                document.getElementById('average-chart-container').style.display = 'block';
            }
        });
    });
}


function onPlaceChangedStart(){
    userloc = autocompleteStart.getPlace();
    
}

function onPlaceChangedEnd(){
    destloc = autocompleteEnd.getPlace();

    
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

        // Update the average hourly availability chart
        const avgResponse = await fetch(`/average_station_data/${stationNumber}`);
        const avgData = await avgResponse.json();
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


function findClosestStationStart(){
    
    stations = {}
    bikeData.forEach(station => {
        if (station.available_bikes != 0){
        stations[station.name] = new google.maps.LatLng(station.latitude, station.longitude)};
    });


    var distances = [];

    for (var stationName in stations) {
        var location = stations[stationName];
        var place = new google.maps.LatLng(userloc.geometry.location.lat(),userloc.geometry.location.lng())
        var distance = google.maps.geometry.spherical.computeDistanceBetween(place, location);
        distances.push({Station:stationName, distance:distance}) 
    }

    

    distances = distances.sort((a, b) => a.distance - b.distance)
    
    result = new google.maps.LatLng(stations[distances[0].Station].lat(), stations[distances[0].Station].lng())
    return result
}

function findClosestStationEnd(){
    
    stations = {}
    bikeData.forEach(station => {
        if (station.available_bikes != 0){
        stations[station.name] = new google.maps.LatLng(station.latitude, station.longitude)};
    });


    var distances = [];

    for (var stationName in stations) {
        var location = stations[stationName];
        var place = new google.maps.LatLng(destloc.geometry.location.lat(),destloc.geometry.location.lng())
        var distance = google.maps.geometry.spherical.computeDistanceBetween(place, location);
        distances.push({Station:stationName, distance:distance}) 
    }

    

    distances = distances.sort((a, b) => a.distance - b.distance)

    result = new google.maps.LatLng(stations[distances[0].Station].lat(), stations[distances[0].Station].lng())
    return result
}


function showRoute() {
    var request1 = {
      origin: new google.maps.LatLng(userloc.geometry.location.lat(),userloc.geometry.location.lng()),
      destination: findClosestStationStart(),
      travelMode: 'WALKING'
    };
  
    var request2 = {
      origin: findClosestStationStart(),
      destination: findClosestStationEnd(),
      travelMode: 'BICYCLING'
    };
  
    var request3 = {
      origin: findClosestStationEnd(),
      destination: new google.maps.LatLng(destloc.geometry.location.lat(),destloc.geometry.location.lng()),
      travelMode: 'WALKING'
    };
  
    directionsService.route(request1, function(result1, status1) {
      if (status1 == 'OK') {
        directionsService.route(request2, function(result2, status2) {
          if (status2 == 'OK') {
            directionsService.route(request3, function(result3, status3) {
              if (status3 == 'OK') {
                // Combine the three legs into a single result
                var combinedResult = result1;
                combinedResult.routes[0].legs.push.apply(combinedResult.routes[0].legs, result2.routes[0].legs);
                combinedResult.routes[0].legs.push.apply(combinedResult.routes[0].legs, result3.routes[0].legs);
  
                // Display the combined result on the map
                directionsRenderer.setDirections(combinedResult);
                directionsRenderer.setMap(map);
                console.log(combinedResult.routes[0].legs[0].duration.text)
              }
            });
          }
        });
      }
    });
  
    
  }

fetchData().then(() => {
    initMap();
    initCharts();
});

function handleDate(){
    var date = document.getElementById('toggle-date')
    if(date.style.display == 'block'){
        date.style.display = 'none'
    }
    else{
        date.style.display='block'
    }
    
}