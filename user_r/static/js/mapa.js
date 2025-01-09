var map; // Definir la variable map aquí 
var marker; // Variable para almacenar el marcador
var defaultCoordinates;
var latitud = parseFloat(document.getElementById('lat').value);
var longitud = parseFloat(document.getElementById('long').value);

// Verificar si latitud y longitud están definidos
if (!isNaN(latitud) && !isNaN(longitud)) {
    defaultCoordinates = [latitud, longitud];
} else {
    defaultCoordinates = [10.492886, -66.780632]; // Coordenadas por defecto
}

// Inicializar el mapa con las coordenadas por defecto
map = L.map('map').setView(defaultCoordinates, 16);

// Añadir la capa de mosaico después de inicializar el mapa
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var redIcon = L.icon({
    iconUrl: redIconUrl, // Usar la variable definida en la plantilla
    shadowUrl: shadowIconUrl,
    iconSize: [38, 95], // tamaño del icono
    shadowSize: [50, 64], // tamaño de la sombra
    iconAnchor: [22, 94], // punto del icono que corresponderá a la ubicación del marcador
    shadowAnchor: [4, 62], // lo mismo para la sombra
    popupAnchor: [-3, -76] // punto desde el cual debería abrirse el popup relativo al icono
});

// Si hay coordenadas, añadir el marcador
if (!isNaN(latitud) && !isNaN(longitud)) {
    marker = L.marker([latitud, longitud], { icon: redIcon }).addTo(map);
}

// Añadir el evento de clic en el mapa
map.on('click', onMapClick);

function onMapClick(event) {
    let latitud = event.latlng.lat; // Obtener la latitud
    let longitud = event.latlng.lng; // Obtener la longitud

    // Si el marcador ya existe, elimínalo
    if (marker) {
        map.removeLayer(marker); // Eliminar el marcador anterior
    }

    // Crear un nuevo marcador y añadirlo al mapa
    marker = L.marker([latitud, longitud], { icon: redIcon }).addTo(map);

    // Actualizar los campos ocultos con la latitud y longitud
    document.getElementById('lat').value = latitud;
    document.getElementById('long').value = longitud;
}