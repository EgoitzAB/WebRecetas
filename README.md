# Proyecto de Página de Recetas

Este es un proyecto colaborativo entre amigos para desarrollar una página web de recetas. Está hecho con Django y con Bootstrap más librerías y código Javascript. Ire mejorando ciertas partes, e ideando el añadirle otras mientras se va subiendo contenido.
Tiene buenas prácticas en ciberseguridad, y todos los requisitos necesarios en una página para cumplir con la ley actualmente. Falta pulir algunos detalles como el robot.txt, la integración de Google Ads y otros pequeños detallitos. Pero son menores y el esqueleto está listo para ser lanzado en la versión Beta.

¡Estamos emocionados de compartir nuestras recetas favoritas y explorar nuevas ideas culinarias juntos!

## Tecnologías Aplicadas

Este proyecto utiliza las siguientes tecnologías:

- **Django:** Un framework web de Python que facilita el desarrollo rápido y limpio de aplicaciones web.
- **PostgreSQL:** Un sistema de gestión de bases de datos relacional robusto y escalable.
- **Django Allauth:** Una biblioteca de autenticación flexible para Django que proporciona características como registro, inicio de sesión y autenticación de dos factores.
- **Django Two Factor Auth:** Una extensión para Django Allauth que agrega autenticación de dos factores a la aplicación.
- **Django OTP:** Un paquete para proporcionar autenticación de un solo uso para Django.
- **Easy Thumbnails:** Una biblioteca para manejar imágenes en Django, que facilita la creación de miniaturas y el procesamiento de imágenes. (Por ahora esto se está haciendo con PIL y Pillow)
- **Taggit:** Una aplicación Django para gestionar etiquetas de forma sencilla y eficiente.(Hay que desarrollar esta parte todavía, pero está instalada para hacerlo próximamente.)
- **Debug Toolbar:** Una herramienta de depuración para Django que proporciona información útil sobre el rendimiento y la estructura de las páginas.
- **Redisboard:** Una interfaz web para interactuar con la base de datos Redis.
- **Cookie Consent:** Una biblioteca para gestionar el consentimiento de las cookies en el sitio web.
- **Django Extensions:** Una colección de extensiones útiles para proyectos Django.
- **Whitenoise:** Un servidor de archivos estáticos para aplicaciones web Django, que mejora el rendimiento y la seguridad al servir archivos estáticos de forma eficiente.
- **Redis:** Una base de datos NoSQL Redis para los sencillos algoritmos de recomendación y contar las vistas de la aplicación en un middleware.
- **PostgreSql:** Una base de datos PostgreSql para la aplicación principal.
- **Whitenoise:** Aplicación para servir las imágenes comprimidas en producción.
- **Select2:** Biblioteca de JS para realizar las búsquedas desde el navbar.
- **AOS:** Biblioteca de JS para añadir animaciones en la página de inicio.
- **PureCounter:** Biblioteca de JS para añadir el conteo de la página principal.
Y todo aquello que me olvido ahora mismo.


## Contribuciones

¡Agradecemos las contribuciones de la comunidad! Si te gustaría contribuir al proyecto, siéntete libre de abrir un problema o enviar una solicitud de extracción. Juntos podemos hacer que esta página de recetas sea aún mejor. Falta Dockerizarlo pero por falta de tiempo haré el Deploy a Apache2 tal y cómo está. También hay pequeños fallos en el Navbar que se solapa con el carousel en algún caso, y algún fallito más que voy corrigiendo. Si quieres, eres libre de mandar un Pull request.

## Licencia

Este proyecto está bajo la Licencia Pública General de GNU (GPLv3), lo que significa que es de software libre y puedes utilizarlo, modificarlo y distribuirlo libremente. Consulta el archivo LICENSE para obtener más información.

Mención a JazzBand y a los templates de ThemeVagon y Templates Jungle.