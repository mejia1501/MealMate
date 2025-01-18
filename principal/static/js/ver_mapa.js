document.addEventListener('DOMContentLoaded', function() {
    var latitud = parseFloat(document.getElementById('latitud').value);
    var longitud = parseFloat(document.getElementById('longitud').value);
    var restaurante = document.getElementById('nombre').value;

    // Inicializar el mapa
    var map = L.map('map').setView([latitud, longitud], 15);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 15,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    var redIcon = L.icon({
        iconUrl: redIconUrl,
        shadowUrl: shadowIconUrl,
        iconSize: [38, 95],
        shadowSize: [50, 64],
        iconAnchor: [22, 94],
        shadowAnchor: [4, 62],
        popupAnchor: [-3, -76]
    });

    // Añadir el marcador al mapa
    L.marker([latitud, longitud], {icon: redIcon})
        .bindPopup(restaurante)
        .addTo(map);
});