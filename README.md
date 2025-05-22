# Traffic Notifications App

A web application that provides traffic notifications based on your location. The app tracks your location periodically and alerts you about traffic conditions in your area.

## Features

- Location tracking every 30 minutes (customizable)
- Real-time traffic information
- Traffic notifications when congestion is detected
- Interactive map with traffic visualization
- Mobile-friendly design

## Requirements

To use this application, you need:

1. A Google Maps API key with the following APIs enabled:
   - Maps JavaScript API
   - Places API
   - Directions API
   - Distance Matrix API

2. A modern web browser that supports:
   - Geolocation API
   - Notifications API
   - JavaScript ES6+

## Setup Instructions

1. Clone this repository
2. Replace `YOUR_API_KEY` in the `index.html` file with your actual Google Maps API key
3. Host the files on a web server or open `index.html` directly in a browser
4. Allow location access when prompted
5. Allow notifications when prompted
6. Click "Start Tracking" to begin receiving traffic updates

## Usage

- **Start Tracking**: Begin location tracking and traffic monitoring
- **Stop Tracking**: Pause location tracking and traffic monitoring
- **Check Interval**: Adjust how frequently your location is checked (in minutes)
- **Test Notification**: Send a test notification to verify permissions

## Mobile Usage

For the best experience on mobile devices:

1. Open the website in your mobile browser
2. Add the page to your home screen
3. Allow the app to run in the background (if supported by your device)
4. Keep location services enabled

## Privacy Note

This application only tracks your location when the "Start Tracking" button is pressed. Your location data is not stored on any server and is only used locally to check traffic conditions.
