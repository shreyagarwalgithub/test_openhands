// Main application functionality
let trackingInterval;
let isTracking = false;

// DOM elements
const startTrackingBtn = document.getElementById('start-tracking');
const stopTrackingBtn = document.getElementById('stop-tracking');
const testNotificationBtn = document.getElementById('test-notification');
const checkIntervalInput = document.getElementById('check-interval');
const currentLocationEl = document.getElementById('current-location');
const lastUpdatedEl = document.getElementById('last-updated');

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    // Set up event listeners
    startTrackingBtn.addEventListener('click', startTracking);
    stopTrackingBtn.addEventListener('click', stopTracking);
    testNotificationBtn.addEventListener('click', testNotification);
    
    // Disable stop button initially
    stopTrackingBtn.disabled = true;
    
    // Check for required permissions
    checkPermissions();
});

// Check for required permissions
function checkPermissions() {
    // Check for geolocation permission
    if (!navigator.geolocation) {
        alert('Geolocation is not supported by your browser');
        disableTracking();
        return;
    }
    
    // Check for notification permission
    if (!('Notification' in window)) {
        alert('Notifications are not supported by your browser');
    } else if (Notification.permission !== 'granted' && Notification.permission !== 'denied') {
        Notification.requestPermission();
    }
    
    // Get initial location
    navigator.geolocation.getCurrentPosition(
        position => {
            updateLocationDisplay(position);
            initMap(position);
        },
        error => {
            handleLocationError(error);
        }
    );
}

// Start location tracking
function startTracking() {
    const interval = parseInt(checkIntervalInput.value) * 60 * 1000; // Convert minutes to milliseconds
    
    if (interval < 5 * 60 * 1000) {
        alert('Please set an interval of at least 5 minutes to avoid excessive battery usage');
        return;
    }
    
    // Get location immediately
    getLocation();
    
    // Set up interval for periodic location checks
    trackingInterval = setInterval(getLocation, interval);
    isTracking = true;
    
    // Update UI
    startTrackingBtn.disabled = true;
    stopTrackingBtn.disabled = false;
    
    // Send notification
    sendNotification('Location Tracking Started', 'You will receive traffic updates based on your location.');
}

// Stop location tracking
function stopTracking() {
    clearInterval(trackingInterval);
    isTracking = false;
    
    // Update UI
    startTrackingBtn.disabled = false;
    stopTrackingBtn.disabled = true;
    
    // Send notification
    sendNotification('Location Tracking Stopped', 'You will no longer receive traffic updates.');
}

// Get current location
function getLocation() {
    navigator.geolocation.getCurrentPosition(
        position => {
            updateLocationDisplay(position);
            
            // If map is initialized, update it
            if (typeof map !== 'undefined') {
                updateMap(position);
            } else {
                initMap(position);
            }
        },
        error => {
            handleLocationError(error);
        },
        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}

// Update location display
function updateLocationDisplay(position) {
    const { latitude, longitude } = position.coords;
    currentLocationEl.textContent = `Lat: ${latitude.toFixed(6)}, Lng: ${longitude.toFixed(6)}`;
    lastUpdatedEl.textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
}

// Handle location errors
function handleLocationError(error) {
    let errorMessage;
    
    switch(error.code) {
        case error.PERMISSION_DENIED:
            errorMessage = 'User denied the request for geolocation.';
            break;
        case error.POSITION_UNAVAILABLE:
            errorMessage = 'Location information is unavailable.';
            break;
        case error.TIMEOUT:
            errorMessage = 'The request to get user location timed out.';
            break;
        case error.UNKNOWN_ERROR:
            errorMessage = 'An unknown error occurred.';
            break;
    }
    
    currentLocationEl.textContent = `Error: ${errorMessage}`;
    console.error('Geolocation error:', error);
    
    if (error.code === error.PERMISSION_DENIED) {
        disableTracking();
    }
}

// Disable tracking functionality
function disableTracking() {
    startTrackingBtn.disabled = true;
    stopTrackingBtn.disabled = true;
    checkIntervalInput.disabled = true;
}

// Send notification
function sendNotification(title, body) {
    if (!('Notification' in window)) {
        console.log('Notifications not supported');
        return;
    }
    
    if (Notification.permission === 'granted') {
        const notification = new Notification(title, {
            body: body,
            icon: 'https://maps.google.com/mapfiles/ms/icons/red-dot.png'
        });
        
        notification.onclick = function() {
            window.focus();
            this.close();
        };
    } else if (Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                sendNotification(title, body);
            }
        });
    }
}

// Send traffic notification
function sendTrafficNotification(trafficInfo) {
    sendNotification('Traffic Alert', trafficInfo);
}

// Test notification
function testNotification() {
    sendNotification('Test Notification', 'This is a test notification. If you see this, notifications are working correctly!');
}