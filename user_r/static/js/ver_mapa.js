var latitud = parseFloat(document.getElementById('latitud').value);
var longitud = parseFloat(document.getElementById('longitud').value);

// Inicializar el mapa
var map = L.map('map').setView([latitud, longitud], 16);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var redIcon = L.icon({
    iconUrl: redIconUrl, // Asegúrate de que la ruta sea correcta
    shadowUrl: shadowIconUrl,
    iconSize: [38, 95], // tamaño del icono
    shadowSize: [50, 64], // tamaño de la sombra
    iconAnchor: [22, 94], // punto del icono que corresponderá a la ubicación del marcador
    shadowAnchor: [4, 62], // lo mismo para la sombra
    popupAnchor: [-3, -76] // punto desde el cual debería abrirse el popup relativo al icono
});

// Añadir el marcador al mapa
L.marker([latitud, longitud], {icon: redIcon}).addTo(map);