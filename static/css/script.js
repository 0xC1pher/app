// static/js/script.js

// Función para mostrar mensajes en la consola
console.log("Archivo script.js cargado correctamente");

// Ejemplo: Mostrar una alerta al hacer clic en un botón
document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".btn-alert");
    buttons.forEach(button => {
        button.addEventListener("click", function () {
            alert("¡Botón presionado!");
        });
    });
});

// Ejemplo: Validación básica de formulario
function validateForm(form) {
    const inputs = form.querySelectorAll("input, textarea, select");
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add("error");
        } else {
            input.classList.remove("error");
        }
    });

    if (!isValid) {
        alert("Por favor, completa todos los campos.");
    }

    return isValid;
}

// Asignar validación a formularios
document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form.validate");
    forms.forEach(form => {
        form.addEventListener("submit", function (event) {
            if (!validateForm(form)) {
                event.preventDefault();
            }
        });
    });
});