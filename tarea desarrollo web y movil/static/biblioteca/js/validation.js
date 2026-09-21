document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form[data-validate]').forEach((form) => {
        form.addEventListener('submit', (event) => {
            let valid = true;
            form.querySelectorAll('.field-error').forEach((error) => { error.textContent = ''; });
            form.querySelectorAll('input, select').forEach((field) => {
                const error = form.querySelector(`[data-error-for="${field.id}"]`);
                if (!error || field.type === 'hidden' || field.type === 'submit') return;
                if (field.required && !field.value.trim()) {
                    error.textContent = 'Este campo es obligatorio.';
                    valid = false;
                } else if (field.type === 'email' && field.value && !field.validity.valid) {
                    error.textContent = 'Ingresa un correo electronico valido.';
                    valid = false;
                } else if (field.name === 'isbn' && field.value && field.value.length < 10) {
                    error.textContent = 'El ISBN debe tener al menos 10 caracteres.';
                    valid = false;
                } else if (field.name === 'anio_publicacion' && field.value && Number(field.value) > new Date().getFullYear()) {
                    error.textContent = 'El ano no puede ser futuro.';
                    valid = false;
                }
            });
            if (!valid) event.preventDefault();
        });
    });
});
