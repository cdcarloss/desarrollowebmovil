// Animación decorativa: una red de puntos verdes conectados por líneas
// que flotan detrás del contenido. No afecta ningún dato de la página ni
// bloquea clics (ver pointer-events:none en el CSS del canvas).
document.addEventListener('DOMContentLoaded', () => {
    const lienzo = document.getElementById('fondo-vectores');
    if (!lienzo || !lienzo.getContext) return;

    // Respeta a quien prefiere menos movimiento en pantalla.
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const ctx = lienzo.getContext('2d');
    const colorLinea = '31, 122, 77'; // mismo verde que --accent en styles.css
    const distanciaMaxima = 140;
    let ancho = 0;
    let alto = 0;
    let particulas = [];

    function medirVentana() {
        ancho = lienzo.width = window.innerWidth;
        alto = lienzo.height = window.innerHeight;
    }

    function crearParticulas() {
        // Menos puntos en pantallas chicas, más en pantallas grandes.
        const cantidad = Math.min(80, Math.floor((ancho * alto) / 16000));
        particulas = Array.from({ length: cantidad }, () => ({
            x: Math.random() * ancho,
            y: Math.random() * alto,
            vx: (Math.random() - 0.5) * 0.35,
            vy: (Math.random() - 0.5) * 0.35,
        }));
    }

    function moverParticulas() {
        particulas.forEach((punto) => {
            punto.x += punto.vx;
            punto.y += punto.vy;
            if (punto.x <= 0 || punto.x >= ancho) punto.vx *= -1;
            if (punto.y <= 0 || punto.y >= alto) punto.vy *= -1;
        });
    }

    function dibujar() {
        ctx.clearRect(0, 0, ancho, alto);
        moverParticulas();

        for (let i = 0; i < particulas.length; i += 1) {
            for (let j = i + 1; j < particulas.length; j += 1) {
                const dx = particulas[i].x - particulas[j].x;
                const dy = particulas[i].y - particulas[j].y;
                const distancia = Math.sqrt(dx * dx + dy * dy);
                if (distancia < distanciaMaxima) {
                    ctx.strokeStyle = `rgba(${colorLinea}, ${1 - distancia / distanciaMaxima})`;
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(particulas[i].x, particulas[i].y);
                    ctx.lineTo(particulas[j].x, particulas[j].y);
                    ctx.stroke();
                }
            }
        }
        particulas.forEach((punto) => {
            ctx.fillStyle = `rgba(${colorLinea}, 0.7)`;
            ctx.beginPath();
            ctx.arc(punto.x, punto.y, 2, 0, Math.PI * 2);
            ctx.fill();
        });

        requestAnimationFrame(dibujar);
    }

    medirVentana();
    crearParticulas();
    dibujar();

    window.addEventListener('resize', () => {
        medirVentana();
        crearParticulas();
    });
});
