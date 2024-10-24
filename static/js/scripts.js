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
    $('#ver-mas-btn').on('click', function () {
        var nextPage = $(this).data('next-page');

        $.ajax({
            url: '?page=' + nextPage,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                // Añadir las nuevas recetas al contenedor de recetas
                $('#recetas-list').append(data.html);

                // Actualizar o eliminar el botón si no hay más páginas
                if (data.has_next) {
                    $('#ver-mas-btn').data('next-page', nextPage + 1);
                } else {
                    $('#ver-mas-container').html('<p>No hay más recetas para mostrar.</p>');
                }
            }
        });
    });
});
