let map;
let routeLine;
let markers = [];

/**
 * Initializes the Leaflet map centered on the Giorgis (City Center) area.
 */
function initMap() {
    // Coordinates match the Giorgis node in Prolog
    map = L.map('map').setView([11.5936, 37.3908], 14);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);
}

// Safer initialization when DOM is fully loaded
document.addEventListener("DOMContentLoaded", initMap);

/**
 * Dictionary of 20 locations in Bahir Dar.
 * Names must match the lowercase_underscore format used in the Prolog backend.
 */
function getCoordinates(place) {
    const locations = {
        giorgis: [11.5936, 37.3908],
        fasilo: [11.5950, 37.3850],
        stadium: [11.5845, 37.3829],
        market: [11.5930, 37.3855],
        tana_shore: [11.6050, 37.3750],
        bdu_main: [11.5972, 37.3958],
        polytechnic: [11.5850, 37.3830],
        technology_campus: [11.5800, 37.4000],
        shumabo: [11.5800, 37.3820],
        abay_bridge: [11.6000, 37.4050],
        airport: [11.6010, 37.3210],
        gish_abay: [11.5900, 37.3900],
        meskel_square: [11.6060, 37.3920],
        zuria: [11.6020, 37.3800],
        bezawit: [11.6150, 37.4100],
        kidane_meheret: [11.5940, 37.4020],
        lemat: [11.6100, 37.3900],
        hidase: [11.5920, 37.3750],
        peda_campus: [11.6120, 37.3880],
        medicine_campus: [11.5800, 37.3790]
    };

    return locations[place] || null;
}

/**
 * Formats underscore names back to readable titles (e.g., "gish_abay" -> "Gish Abay").
 */
function formatName(name) {
    return name.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
}

/**
 * Draws the computed path on the map with markers and a polyline.
 */
function drawRoute(path) {
    if (!map) {
        console.error("Map not initialized yet");
        return;
    }

    clearMap();

    let latlngs = [];

    path.forEach((place, i) => {
        const coords = getCoordinates(place);

        if (!coords) {
            console.warn("Missing coords in map.js for:", place);
            return;
        }

        latlngs.push(coords);

        // Add individual markers for each node in the path
        let marker = L.marker(coords)
            .addTo(map)
            .bindPopup(`<b>${formatName(place)}</b><br>Step ${i + 1}`);

        markers.push(marker);
    });

    if (latlngs.length === 0) return;

    // Draw the line connecting all points
    routeLine = L.polyline(latlngs, {
        color: 'blue',
        weight: 5,
        opacity: 0.7
    }).addTo(map);

    // Zoom the map to fit the entire route
    map.fitBounds(routeLine.getBounds());
}

/**
 * Clears existing routes and markers before drawing a new search result.
 */
function clearMap() {
    if (routeLine) map.removeLayer(routeLine);

    markers.forEach(m => map.removeLayer(m));
    markers = [];
}