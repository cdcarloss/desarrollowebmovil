// Validación de formularios en el cliente.
// Se aplica a todo <form data-validate>. El servidor vuelve a validar igualmente.

const REGEX_CORREO = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const REGEX_TELEFONO = /^\+?\d{8,12}$/;

// Devuelve el mensaje de error del campo, o '' si es válido.
function validarCampo(campo) {
    const valor = campo.value.trim();

    // 1. Campo obligatorio (y selección obligatoria en los <select>)
    if (campo.required && valor === '') {
        return campo.tagName === 'SELECT' ? 'Selecciona una opción.' : 'Este campo es obligatorio.';
    }
    if (valor === '') return '';

    // 2. Largo mínimo
    if (campo.minLength > 0 && valor.length < campo.minLength) {
        return `Debe tener al menos ${campo.minLength} caracteres.`;
    }

    // 3. Formato de correo
    if (campo.type === 'email' && !REGEX_CORREO.test(valor)) {
        return 'Ingresa un correo válido, por ejemplo nombre@dominio.cl.';
    }

    // 4. Formato de teléfono
    if (campo.dataset.formato === 'telefono' && !REGEX_TELEFONO.test(valor)) {
        return 'Ingresa un teléfono válido, por ejemplo +56912345678.';
    }

    // 5. Rango numérico (atributos min y max del input)
    if (campo.type === 'number') {
        const numero = Number(valor);
        if (campo.min !== '' && numero < Number(campo.min)) {
            return `El valor mínimo es ${campo.min}.`;
        }
        if (campo.max !== '' && numero > Number(campo.max)) {
            return `El valor máximo es ${campo.max}.`;
        }
    }
    return '';
}

function mostrarError(campo, mensaje) {
    const contenedor = campo.closest('form').querySelector(`[data-error-for="${campo.id}"]`);
    if (contenedor) contenedor.textContent = mensaje;
    campo.setAttribute('aria-invalid', mensaje ? 'true' : 'false');
}

function iniciarValidacion(formulario) {
    const campos = Array.from(formulario.querySelectorAll('input, select, textarea'))
        .filter((campo) => campo.type !== 'hidden' && campo.type !== 'submit');

    // Al salir de un campo se valida solo ese campo
    campos.forEach((campo) => {
        campo.addEventListener('blur', () => mostrarError(campo, validarCampo(campo)));
        campo.addEventListener('input', () => {
            if (campo.getAttribute('aria-invalid') === 'true') mostrarError(campo, validarCampo(campo));
        });
    });

    // Al enviar se validan todos; si alguno falla, se bloquea el envío
    formulario.addEventListener('submit', (evento) => {
        let primerInvalido = null;
        campos.forEach((campo) => {
            const mensaje = validarCampo(campo);
            mostrarError(campo, mensaje);
            if (mensaje && !primerInvalido) primerInvalido = campo;
        });
        if (primerInvalido) {
            evento.preventDefault();
            primerInvalido.focus();
        }
    });
}

// Estado "cargando": al filtrar un listado se oculta la tabla y se muestra el aviso
function iniciarEstadoCargando(formulario) {
    formulario.addEventListener('submit', () => {
        const aviso = document.getElementById('estado-cargando');
        const resultados = document.getElementById('resultados');
        if (aviso) aviso.hidden = false;
        if (resultados) resultados.hidden = true;
    });
}

// Selección exclusiva entre dos campos: exactamente uno debe tener valor.
// Se usa en el formulario de venta (un libro O un juego, nunca ambos ni ninguno).
function iniciarSeleccionExclusiva(formulario) {
    const ids = formulario.dataset.exclusivo.split(',').map((id) => id.trim());
    const campos = ids.map((id) => document.getElementById(id));
    const contenedorError = document.getElementById(formulario.dataset.errorExclusivo);

    function validar() {
        const seleccionados = campos.filter((campo) => campo.value !== '').length;
        const valido = seleccionados === 1;
        if (contenedorError) {
            contenedorError.textContent = valido ? '' : 'Elige un libro o un juego de mesa (no ambos, no ninguno).';
        }
        return valido;
    }

    campos.forEach((campo) => campo.addEventListener('change', validar));
    formulario.addEventListener('submit', (evento) => {
        if (!validar()) evento.preventDefault();
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form[data-validate]').forEach(iniciarValidacion);
    document.querySelectorAll('form[data-cargando]').forEach(iniciarEstadoCargando);
    document.querySelectorAll('form[data-exclusivo]').forEach(iniciarSeleccionExclusiva);
});
