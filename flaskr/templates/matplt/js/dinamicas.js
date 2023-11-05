// Función para abrir la imagen en pantalla completa
function openFullScreen() {
    const img = document.querySelector(".full-screen-image");
    img.style.width = "100%";
    img.style.height = "100%";
    img.style.position = "fixed";
    img.style.top = "0";
    img.style.left = "0";
    img.style.zIndex = "9999";
}

// Función para cerrar la imagen a pantalla completa
function closeFullScreen() {
    const img = document.querySelector(".full-screen-image");
    img.style.width = "auto";
    img.style.height = "auto";
    img.style.position = "static";
    img.style.zIndex = "0";
}
