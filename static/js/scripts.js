/*function toggleCardSize(button) {
    var cardBody = button.parentElement.previousElementSibling;
    console.log('CardBody:', cardBody);
    if (cardBody.classList.contains('collapsed')) {
        console.log('CardBody is collapsed');
        cardBody.classList.remove('collapsed');
        cardBody.classList.add('expanded');
        button.textContent = 'Retract';
    } else {
        console.log('CardBody is expanded');
        cardBody.classList.remove('expanded');
        cardBody.classList.add('collapsed');
        button.textContent = 'Expand';
    }
};

$(document).ready(function() {
    $(document).on('click', '.toggle-button', function() {
        console.log('Button clicked');
        toggleCardSize(this);
    });
}); */

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

// Select2 for the main searching feature
$(document).ready(function() {
    $('.search-field').select2({
        ajax: {
            url: autocompleteUrl,
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term, // search term
                };
            },
            processResults: function (data) {
                return {
                    results: data,
                };
            },
        },
        minimumInputLength: 3,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        console.log('Selected data:', data);
        window.location.href = '/receta_detalle/' + data.id + '/';  // Redirige al usuario a la página de detalles de la receta seleccionada
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