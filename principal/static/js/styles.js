const menu1 = document.querySelector('.hamburguesa');
const menu = document.querySelector('.menu');
const imagenes = document.querySelectorAll('img');
const btnTodos = document.querySelector('.todos');
const btnEnsaladas = document.querySelector('.ensaladas');
const btnPasta = document.querySelector('.pasta');
const btnPizza = document.querySelector('.pizza');
const btnPostres = document.querySelector('.postres');
const btnHambur = document.querySelector('.hambur');
const btnSushi = document.querySelector('.sushi');
const contenedorPlatillos = document.querySelector('.platillos');

document.addEventListener('DOMContentLoaded', ()=>{
    eventos();
    platillos();
});

const eventos = () => {
    menu1.addEventListener('click', abrirMenu);
}

const abrirMenu = () => {
    menu.classList.remove('ocultar');
    botonCerrar();
}

const botonCerrar = () => {
    const btnCerrar = document.createElement('p');
    const overlay = document.createElement('div');
    overlay.classList.add('pantalla-completa');
    const body = document.querySelector('body');
    if(document.querySelectorAll('.pantalla-completa').lenght > 0) return;
    body.appendChild(overlay);
    btnCerrar.textContent = 'x';
    btnCerrar.classList.add('btn-cerrar');
    
    // while(navegacion.children[5]){
    //     navegacion.removeChild(navegacion.children[5]);
    // }
    menu.appendChild(btnCerrar);
    cerrarMenu(btnCerrar, overlay);
}

const observer = new IntersectionObserver ((entries, observer)=>{
    entries.forEach(entry=>{
        if(entry.isIntersecting){
            const imagen=entry.target;
            
            observer.unobserve(imagen);
        }
    });
});

imagenes.forEach(imagen => {
    
    observer.observe(imagen);
});

const cerrarMenu = (boton, overlay) => {
    boton.addEventListener('click', ()=>{
        menu.classList.add('ocultar');
        overlay.remove();
        boton.remove();
    });

    overlay.onclick = function () {
        overlay.remove();
        menu.classList.add('ocultar');
        boton.remove();
    }
}

const platillos = () => {
    let platillosArreglo = [];
    const platillos = document.querySelectorAll('.platillo');

    platillos.forEach(platillo=> platillosArreglo = [...platillosArreglo,platillo]);

    const ensaladas = platillosArreglo.filter(ensalada=> ensalada.getAttribute('data-platillo') === 'ensalada');
    const pastas = platillosArreglo.filter(pasta => pasta.getAttribute('data-platillo') === 'pasta');
    const pizzas = platillosArreglo.filter(pizza => pizza.getAttribute('data-platillo') === 'pizza');
    const postres = platillosArreglo.filter(postre=> postre.getAttribute('data-platillo') === 'postre');
    const hambur = platillosArreglo.filter(hambur=> hambur.getAttribute('data-platillo') === 'hambur');
    const sushi = platillosArreglo.filter(sushi=> sushi.getAttribute('data-platillo') === 'sushi');

    mostrarPlatillos(ensaladas, pastas, pizzas, postres, hambur, sushi, platillosArreglo);
}

const mostrarPlatillos = (ensaladas, pastas, pizzas, postres, hambur, sushi, todos) =>{
    btnEnsaladas.addEventListener('click', ()=>{
        limpiarHtml(contenedorPlatillos);
        ensaladas.forEach(ensalada=> contenedorPlatillos.appendChild(ensalada));
    });

    btnPasta.addEventListener('click', ()=>{
        limpiarHtml(contenedorPlatillos);
        pastas.forEach(pasta=> contenedorPlatillos.appendChild(pasta));
    });

    btnPizza.addEventListener('click', ()=>{
        limpiarHtml(contenedorPlatillos);
        pizzas.forEach(pizza=> contenedorPlatillos.appendChild(pizza));
    });
    btnPostres.addEventListener('click', ()=>{
        limpiarHtml(contenedorPlatillos);
        postres.forEach(postre=> contenedorPlatillos.appendChild(postre));
    });
    btnHambur.addEventListener('click', ()=>{
        limpiarHtml(contenedorPlatillos);
        hambur.forEach(hambur=> contenedorPlatillos.appendChild(hambur));
    });
    btnSushi.addEventListener('click', ()=>{
        limpiarHtml(contenedorPlatillos);
        sushi.forEach(sushi=> contenedorPlatillos.appendChild(sushi));
    });
    btnTodos.addEventListener('click',()=>{
        limpiarHtml(contenedorPlatillos);
        todos.forEach(todo=> contenedorPlatillos.appendChild(todo));
    });
}

const limpiarHtml = (contenedor) =>{
    while(contenedor.firstChild){
        contenedor.removeChild(contenedor.firstChild);
    }
}