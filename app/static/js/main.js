// Puedes añadir cualquier lógica de JavaScript aquí para mejorar la UX
document.addEventListener('DOMContentLoaded', () => {
    // Ejemplo: desvanecer mensajes flash después de unos segundos
    const flashes = document.querySelector('.flashes');
    if (flashes) {
        setTimeout(() => {
            flashes.style.opacity = 0;
            flashes.style.transition = 'opacity 0.5s ease-out';
            setTimeout(() => flashes.remove(), 500);
        }, 3000); // Desvanecer después de 3 segundos
    }
});