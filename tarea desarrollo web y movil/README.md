# Biblioteca Horizonte

Aplicacion web Django para administrar el catalogo de una biblioteca ficticia. Este proyecto se organiza con el patron MVT y utiliza PostgreSQL como motor de base de datos.

## Estructura

```text
.
|-- manage.py
|-- requirements.txt
|-- .env.example
|-- Dockerfile
|-- docker-compose.yml
|-- biblioteca_project/
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|-- biblioteca/
|   |-- models.py
|   |-- forms.py
|   |-- views.py
|   |-- urls.py
|   |-- admin.py
|   |-- migrations/
|   `-- templates/
|-- templates/biblioteca/
|-- static/biblioteca/css/
|-- static/biblioteca/js/
`-- docs/modelo.md
```

## Entidades y relaciones

- `Autor`: nombre y nacionalidad.
- `Categoria`: clasificacion reutilizable para libros.
- `Libro`: titulo, ISBN, ano, ejemplares, autor y categorias.
- `Socio`: persona que utiliza la biblioteca.
- `Prestamo`: relacion entre un socio y un libro.

Las decisiones de borrado estan documentadas en [docs/modelo.md](docs/modelo.md). `Autor` y `Libro` usan `PROTECT` para conservar referencias importantes; `Socio` usa `CASCADE` porque sus prestamos dependen de su existencia.

## Instalacion

### Opcion recomendada: Docker

Docker Compose crea PostgreSQL, espera a que la base este disponible, ejecuta las migraciones, carga datos de demostracion y levanta Django.

1. Copiar `.env.example` a `.env` si no existe.
2. Ejecutar:

   ```powershell
   docker compose up --build
   ```

3. Abrir `http://localhost:8000/`.

Usuarios precargados para la revision:

- Administrador: `admin` / `Admin12345!`
- Usuario comun: `lector` / `Lector12345!`

Para detener los contenedores:

```powershell
docker compose down
```

Para borrar tambien los datos de PostgreSQL y comenzar desde cero:

```powershell
docker compose down -v
```

### Instalacion manual

1. Crear y activar un entorno virtual:

   ```powershell
   python -m venv .venv
   .venv\\Scripts\\Activate.ps1
   ```

2. Instalar dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

3. Crear una base y usuario en PostgreSQL:

   ```sql
   CREATE USER biblioteca_user WITH PASSWORD 'cambia-esta-clave';
   CREATE DATABASE biblioteca_db OWNER biblioteca_user;
   GRANT ALL PRIVILEGES ON DATABASE biblioteca_db TO biblioteca_user;
   ```

4. Copiar `.env.example` a `.env`, cambiar `DB_HOST` a `localhost` y completar las credenciales locales.

5. Aplicar migraciones y crear administrador:

   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

6. Abrir `http://127.0.0.1:8000/`. El sitio exige autenticacion y redirige al login.

## Usuarios de prueba

Crear en cada entorno con `createsuperuser` un usuario administrador. Para el usuario comun, crear una cuenta desde el panel de administracion en `/admin/`. No se deben guardar contrasenas reales en el repositorio; completar aqui los usuarios acordados antes de entregar.

En el flujo Docker los usuarios de revision los crea automaticamente el comando `seed_demo`. Las contrasenas incluidas son solo para desarrollo local y deben cambiarse antes de una entrega publica.

## Funcionalidad inicial

- Login y logout con autenticacion nativa de Django.
- Pagina de inicio protegida.
- CRUD completo de libros.
- Filtro del catalogo por categoria relacionada.
- Desplegables y opciones de categorias/autor poblados desde la base de datos.
- Validacion cliente externa en `static/biblioteca/js/validation.js` y validacion de dominio en los modelos.
- Panel admin personalizado para libros y prestamos.

## Base de datos y respaldo

La entrega final debe incluir un respaldo PostgreSQL con los datos reales de prueba:

```powershell
pg_dump -U biblioteca_user -d biblioteca_db -f respaldo_biblioteca.sql
```

Cargarlo con:

```powershell
psql -U biblioteca_user -d biblioteca_db -f respaldo_biblioteca.sql
```
