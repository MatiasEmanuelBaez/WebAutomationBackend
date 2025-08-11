# Web Automation Backend

El proyecto consiste en un backend desarrollado en Python para automatizar la extracción de datos de diferentes páginas web utilizando *Playwright*. La aplicación extrae de cada sitio los datos más relevantes: nombre del producto, descripción, precio e imagen, y los almacena en una base de datos *PostgreSQL*.

>Actualmente el código soporta la automatización de extracción de datos de dos páginas web, pero está es fácilmente escalable a más sitios.

>El proyecto está integrado con Docker para poder ejecutarlo rápidamente, sin problemas de configuración o dependencias.


## Tecnologías utilizadas

* Docker
* Python
* Playwright
* PostgreSQL
* API REST

## Base de datos

Para almacenar la información extraída se utiliza una tabla productos donde se guarda toda la información relevante de cada producto, y una tabla tasks que mantiene un registro de cada ejecución del scraper.

<img src="misc\db.png" width="600" />

## Páginas soportadas

* https://www.saucedemo.com/
* https://practicesoftwaretesting.com/

## Instalación y ejecución

Gracias a Docker, las pruebas pueden realizarse fácilmente siguiendo estos pasos:

1. Clonar el repositorio.
2. Modificar, si es necesario, el archivo *.env* con la configuración deseada.
3. Tener Docker instalado y ejecutándose.
4. Desde consola, levantar el proyecto con:
~~~ 
docker-compose up --build
~~~
5. Podremos acceder a la API desde http://localhost:8000



---------------------------
