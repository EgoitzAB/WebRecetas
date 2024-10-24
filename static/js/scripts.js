window.addEventListener('DOMContentLoaded', event => {
    // Navbar shrink function
    var navbarShrink = function () {
    const navbarCollapsible = document.body.querySelector('#mainNav');
    if (!navbarCollapsible) {
        return;
    }
    if (window.scrollY === 0) {
        navbarCollapsible.classList.remove('navbar-shrink')
    } else {
        navbarCollapsible.classList.add('navbar-shrink')
    }
};
    // Shrink the navbar
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);
//  Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

// Collapse responsive navbar when toggler is visible
const navbarToggler = document.body.querySelector('.navbar-toggler');
const responsiveNavItems = [].slice.call(
    document.querySelectorAll('#navbarResponsive .nav-link')
);
responsiveNavItems.map(function (responsiveNavItem) {
    responsiveNavItem.addEventListener('click', () => {
        if (window.getComputedStyle(navbarToggler).display !== 'none') {
            navbarToggler.click();
        }
    });
});

});

$(document).ready(function() {
    // Inicializa Select2 en el campo de búsqueda principal
    $('.search-field').select2({
        ajax: {
            url: autocompleteUrl,
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term, // término de búsqueda
                };
            },
            processResults: function (data) {
                console.log('Datos de respuesta del servidor para principal:', data);
                return {
                    results: data,
                };
            },
        },
        minimumInputLength: 3,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        console.log('Selected data:', data);
        window.location.href = '/receta_detalle/' + data.id + '/';
    });

    // Evento que se dispara cuando el offcanvas se muestra
    $('#offcanvasNavbar2').on('shown.bs.offcanvas', function () {
        console.log("Offcanvas mostrado");
            // Inicializa Select2 en el campo de búsqueda del offcanvas
            $('.search-field').select2({
                ajax: {
                    url: autocompleteUrl,
                    dataType: 'json',
                    delay: 250,
                    data: function (params) {
                        return {
                            q: params.term, // término de búsqueda
                        };
                    },
                    processResults: function (data) {
                        console.log('Datos de respuesta del servidor para offcanvas:', data);
                        return {
                            results: data,
                        };
                    },
                },
                dropdownParent: $('#offcanvasNavbar2'),
                minimumInputLength: 3,
            }).on('select2:select', function (e) {
                var data = e.params.data;
                console.log('Selected data:', data);
                window.location.href = '/receta_detalle/' + data.id + '/';
            });
    });
});


window.addEventListener('scroll', function() {
    var timelineElements = document.querySelectorAll('.timeline > li');

    timelineElements.forEach(function(element) {
        var position = element.getBoundingClientRect();

        // Comprueba si el elemento está en la vista
        if(position.top >= 0 && position.bottom <= window.innerHeight) {
            element.classList.add('visible');
        }
    });
});


$(document).ready(function() {
    $('.timeline.card-hidden').hide(); // Ocultar los elementos ocultos al cargar la página
    $('.timeline-link').click(function(event) {
        event.preventDefault(); // Evitar que el enlace realice su acción predeterminada
        $('.timeline.card-hidden').slideDown(); // Mostrar los elementos ocultos al hacer clic en el último elemento de la línea de tiempo
        $(this).hide(); // Ocultar el último elemento de la línea de tiempo después de mostrar los elementos ocultos
    });
});

$(document).ready(function () {
    AOS.init({
    duration: 1200,
    easing: "ease-in-out",
    once: true,
    mirror: false,
    });
    if (typeof PureCounter !== 'undefined') {
        new PureCounter({
            once: false,
            pulse: false,
            formater: "us-US",
            separator: true,
            decimals: 0,
            delay: 10,
        });
    }
});

$(document).ready(function () {
    var offset = 12; // Cantidad inicial de recetas cargadas

    $('#ver-mas-btn').on('click', function () {
        $.ajax({
            url: '?offset=' + offset, // Enviamos el offset para cargar más recetas
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                // Añadimos las nuevas recetas al contenedor
                $('#recetas-list').append(data.html);

                // Aumentamos el offset para la siguiente carga
                offset += 12;

                // Si no quedan más recetas, ocultamos el botón "Ver más"
                if (!data.quedan_mas) {
                    $('#ver-mas-container').remove();
                }
            }
        });
    });
});

// Función para obtener el valor del token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Obtener el token CSRF
const csrfToken = getCookie('csrftoken');

// Función para manejar la acción de agregar o quitar de favoritos
function toggleFavorito(button) {
    const recetaId = button.getAttribute('data-receta-id');
    const isAdding = button.innerText.includes('Agregar');

    fetch(isAdding ? `/favorito/agregar/${recetaId}/` : `/favorito/eliminar/${recetaId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Cambiar el texto del botón dependiendo de la acción
            if (data.action === 'added') {
                button.innerText = 'Quitar de favoritos';
            } else {
                button.innerText = 'Agregar a favoritos';
            }
        } else {
            console.error('Error al procesar la solicitud');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
