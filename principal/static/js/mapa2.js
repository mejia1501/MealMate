var map; // Definir la variable map aquí 
var marker; // Variable para almacenar el marcador
var defaultCoordinates = [10.492886, -66.780632]; // Coordenadas por defecto

// Obtener los valores de latitud y longitud desde los campos ocultos
var latitud = parseFloat(document.getElementById('lat').value);
var longitud = parseFloat(document.getElementById('long').value);
var redIcon = L.icon({
    iconUrl: redIconUrl, // Usar la variable definida en la plantilla
    shadowUrl: shadowIconUrl,
    iconSize: [38, 95], // tamaño del icono
    shadowSize: [50, 64], // tamaño de la sombra
    iconAnchor: [22, 94], // punto del icono que corresponderá a la ubicación del marcador
    shadowAnchor: [4, 62], // lo mismo para la sombra
    popupAnchor: [-3, -76] // punto desde el cual debería abrirse el popup relativo al icono
});
// Inicializar el mapa
function initializeMap(coordinates) {
    map = L.map('map').setView(coordinates, 16);

    // Añadir la capa de mosaico después de inicializar el mapa
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    // Crear un marcador en las coordenadas proporcionadas
    marker = L.marker(coordinates, { icon: redIcon }).addTo(map);

    // Añadir el evento de clic en el mapa
    map.on('click', onMapClick);
}

// Verificar si latitud y longitud están definidos
if (!isNaN(latitud) && !isNaN(longitud)) {
    // Si hay coordenadas válidas, inicializar el mapa con ellas
    initializeMap([latitud, longitud]);
} else {
    // Intentar obtener la ubicación actual del usuario
    navigator.geolocation.getCurrentPosition((position) => {
        // Inicializar el mapa con la posición actual
        initializeMap([position.coords.latitude, position.coords.longitude]);
    }, (error) => {
        console.error('Error al obtener la ubicación:', error);
        // Inicializar el mapa con las coordenadas por defecto
        initializeMap(defaultCoordinates);
    });
}

// Función para manejar el clic en el mapa
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