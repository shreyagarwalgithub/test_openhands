// Map and traffic related functionality
let map;
let trafficLayer;
let marker;
let directionsService;
let directionsRenderer;

// Initialize the map
function initMap(position) {
    const currentLocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };

    // Create map centered at current location
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: currentLocation,
    });

    // Add traffic layer
    trafficLayer = new google.maps.TrafficLayer();
    trafficLayer.setMap(map);

    // Add marker for current location
    marker = new google.maps.Marker({
        position: currentLocation,
        map: map,
        title: "Your Location"
    });

    // Initialize directions service
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        suppressMarkers: true
    });

    // Check traffic conditions
    checkTrafficConditions(currentLocation);
}

// Update map with new location
function updateMap(position) {
    const newLocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };

    // Update map center
    map.setCenter(newLocation);

    // Update marker position
    marker.setPosition(newLocation);

    // Check traffic conditions
    checkTrafficConditions(newLocation);
}

// Check traffic conditions around the current location
function checkTrafficConditions(location) {
    // Get nearby places to simulate destinations
    const placesService = new google.maps.places.PlacesService(map);
    
    const request = {
        location: location,
        radius: 5000,  // 5km radius
        type: ['point_of_interest']
    };

    placesService.nearbySearch(request, (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK && results.length > 0) {
            // Take a random destination from the results
            const randomIndex = Math.floor(Math.random() * Math.min(results.length, 5));
            const destination = results[randomIndex].geometry.location;
            
            // Calculate route and check traffic
            calculateRoute(location, destination);
        } else {
            document.getElementById('traffic-info').textContent = 
                'Unable to find nearby destinations to check traffic.';
        }
    });
}

// Calculate route and check traffic conditions
function calculateRoute(origin, destination) {
    const request = {
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.DRIVING,
        drivingOptions: {
            departureTime: new Date(),
            trafficModel: google.maps.TrafficModel.BEST_GUESS
        }
    };

    directionsService.route(request, (result, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
            directionsRenderer.setDirections(result);
            
            // Get traffic information
            const route = result.routes[0];
            const leg = route.legs[0];
            
            // Calculate traffic delay
            const durationInTraffic = leg.duration_in_traffic.value;
            const normalDuration = leg.duration.value;
            const delay = durationInTraffic - normalDuration;
            
            // Update traffic info
            let trafficStatus = '';
            if (delay > 600) { // More than 10 minutes delay
                trafficStatus = `Heavy traffic detected! Delay of ${Math.round(delay/60)} minutes.`;
                sendTrafficNotification(trafficStatus);
            } else if (delay > 300) { // 5-10 minutes delay
                trafficStatus = `Moderate traffic. Delay of ${Math.round(delay/60)} minutes.`;
            } else {
                trafficStatus = 'Traffic is flowing normally.';
            }
            
            document.getElementById('traffic-info').innerHTML = 
                `<strong>Destination:</strong> ${leg.end_address.split(',')[0]}<br>` +
                `<strong>Distance:</strong> ${leg.distance.text}<br>` +
                `<strong>Normal duration:</strong> ${leg.duration.text}<br>` +
                `<strong>Duration in traffic:</strong> ${leg.duration_in_traffic.text}<br>` +
                `<strong>Status:</strong> ${trafficStatus}`;
        } else {
            document.getElementById('traffic-info').textContent = 
                'Unable to calculate route and traffic conditions.';
        }
    });
}