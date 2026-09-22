# Modelo de datos

```mermaid
erDiagram
    AUTOR ||--o{ LIBRO : "escribe (1:N)"
    LIBRO ||--|| LIBROFISICO : "subtipo"
    LIBRO ||--|| LIBROEBOOK : "subtipo"
    LIBRO ||--o{ PRESTAMO : "se presta en (1:N, opcional)"
    JUEGOMESA ||--o{ PRESTAMO : "se presta en (1:N, opcional)"
    SOCIO ||--o{ PRESTAMO : "pide (1:N)"
    EMPLEADO ||--o{ PRESTAMO : "atiende (1:N, opcional)"
    USUARIO ||--o| SOCIO : "vincula (1:1, opcional)"
    USUARIO ||--|| PERFIL : "tiene (1:1)"
    LIBRO ||--o{ COMENTARIO : "recibe opiniones (1:N)"
    USUARIO ||--o{ COMENTARIO : "escribe (1:N)"

    AUTOR {
        bigint id PK
        varchar nombre
        varchar nacionalidad
    }
    LIBRO {
        bigint id PK
        varchar titulo
        varchar isbn UK
        int anio_publicacion
        int stock "ejemplares disponibles"
        varchar tipo "FISICO o EBOOK"
        bigint autor_id FK
    }
    LIBROFISICO {
        bigint libro_ptr_id PK_FK "= LIBRO.id"
        varchar ubicacion
    }
    LIBROEBOOK {
        bigint libro_ptr_id PK_FK "= LIBRO.id"
        varchar formato_archivo
        int tamano_mb
    }
    JUEGOMESA {
        bigint id PK
        varchar nombre
        varchar marca
        varchar categoria
        int jugadores_min
        int jugadores_max
        int edad_minima
        int stock
    }
    SOCIO {
        bigint id PK
        varchar nombre
        varchar correo UK
        varchar telefono
        date fecha_registro
        bigint usuario_id FK "nullable, unique"
    }
    USUARIO {
        bigint id PK
        varchar username UK
        varchar password
    }
    PERFIL {
        bigint id PK
        bigint usuario_id FK UK
        varchar foto
        varchar descripcion
    }
    COMENTARIO {
        bigint id PK
        bigint libro_id FK
        bigint usuario_id FK
        text texto
        datetime fecha
    }
    EMPLEADO {
        bigint id PK
        varchar nombre
        varchar correo UK
        varchar cargo
        bool activo
    }
    PRESTAMO {
        bigint id PK
        bigint libro_id FK "nullable"
        bigint juego_id FK "nullable"
        bigint socio_id FK
        bigint empleado_id FK "nullable"
        date fecha_prestamo
        date fecha_devolucion_prevista
        date fecha_devolucion_real
        bool devuelto
    }
```

## Súper tipo y subtipos: `Libro`

`Libro` es el **súper tipo**: toda fila de la tabla `biblioteca_libro` es un libro, físico o digital. `LibroFisico` y `LibroEbook` son **subtipos** hechos con herencia de tablas de Django (herencia multi-tabla): cada uno tiene su propia tabla, unida a `Libro` por una clave primaria compartida (`libro_ptr_id`). El campo `tipo` en `Libro` guarda cuál es cuál.

- **Comunes** (viven en `Libro`): título, ISBN, año, autor, ejemplares disponibles.
- **`LibroFisico`** agrega: ubicación en la estantería.
- **`LibroEbook`** agrega: formato de archivo (EPUB/PDF/MOBI) y tamaño en MB.

`JuegoMesa` **no** es un subtipo de `Libro`: es una tabla independiente. Lo que sí comparten `Libro` y `JuegoMesa` es el comportamiento de "cosa que se puede prestar" (ejemplares disponibles, descontar/reponer), factorizado en `Prestable`, una clase **abstracta** (no crea tabla propia).

## Cardinalidades y `on_delete`

| Relación | Cardinalidad | `on_delete` | Justificación |
|---|---|---|---|
| `Libro.autor` → `Autor` | N:1 | `PROTECT` | Un autor con libros en el catálogo no se puede borrar por accidente. |
| `Prestamo.libro` → `Libro` | N:1 (opcional) | `PROTECT` | El préstamo es un registro histórico: el libro prestado no puede desaparecer. |
| `Prestamo.juego` → `JuegoMesa` | N:1 (opcional) | `PROTECT` | Mismo motivo, aplicado a los juegos de mesa. |
| `Prestamo.socio` → `Socio` | N:1 | `CASCADE` | Si un socio se elimina de la biblioteca, no tiene sentido conservar el historial de préstamos de alguien que ya no existe como miembro. |
| `Prestamo.empleado` → `Empleado` | N:1 (opcional) | `PROTECT` | Cuando un bibliotecario atiende el préstamo, debe quedar registrado quién fue. Para retirarlo se marca `activo=False`, no se elimina. |
| `Socio.usuario` → `User` | 1:1 (opcional) | `SET_NULL` | Si se borra la cuenta de acceso, la ficha del socio (y su historial) se conserva; solo pierde el acceso web. |
| `Perfil.usuario` → `User` | 1:1 | `CASCADE` | Un perfil no existe sin la cuenta a la que describe. |
| `Comentario.libro` → `Libro` | N:1 | `CASCADE` | Un libro sin préstamos sí puede eliminarse; si eso pasa, sus opiniones ya no tienen sentido. |
| `Comentario.usuario` → `User` | N:1 | `CASCADE` | Si se borra la cuenta, sus opiniones se eliminan con ella. |

`Prestamo.libro` y `Prestamo.juego` son ambos opcionales (`null=True, blank=True`), pero el modelo exige en `clean()` que se llene **exactamente uno**: un préstamo es de un libro o de un juego, nunca de ambos ni de ninguno. `Prestamo.empleado` también es opcional: queda vacío cuando el propio socio pide el préstamo desde su lista en el portal (ver más abajo), y con valor cuando un bibliotecario lo registra en el mesón.

## Reglas de negocio (viven en `models.py`)

- `Libro.clean()`: el año de publicación no puede ser futuro.
- `JuegoMesa.clean()`: el máximo de jugadores no puede ser menor que el mínimo.
- `Prestamo.clean()`: exige exactamente un producto (libro o juego), rechaza un empleado inactivo y valida que haya ejemplares disponibles.
- `Prestamo.save()`: en una transacción bloquea la fila del producto, calcula la fecha de devolución prevista (14 días para libros físicos, 7 para ebooks, 10 para juegos de mesa) y descuenta el stock.
- `Prestamo.marcar_devuelto()`: repone el stock, marca `devuelto=True` y guarda la fecha real de devolución. El registro **no se borra**: queda como historial.
- `Prestamo.dias_de_atraso` / `esta_atrasado`: calculan el atraso comparando la fecha de devolución prevista con hoy.
- `Prestable.descontar_stock()` / `reponer_stock()`: comportamiento compartido por `Libro` y `JuegoMesa`.

## "Mi lista de préstamos" (carrito)

Para pedir varios títulos a la vez sin pasar por el mesón, el sitio incluye una lista temporal que vive en la **sesión** del navegador (`biblioteca/carrito.py`), no en la base de datos: es un borrador de la visita. Al confirmar, cada línea se convierte en una fila permanente de `Prestamo` con `empleado` vacío y `socio` igual al socio vinculado a la cuenta (`request.user.socio`). Esto exige seguir con sesión iniciada (como el resto del sitio, según R3 del taller): la lista es solo una forma más rápida de generar préstamos, no una manera de saltarse el login.

## Perfil, vínculo con `Socio` y foro de opiniones

- `Perfil` extiende a `auth.User` con una foto y una descripción corta. Como Django no permite agregar campos directamente al modelo `User`, se usa el patrón estándar de un modelo aparte con `OneToOneField`. Se crea automáticamente con una señal `post_save` sobre `User` (`biblioteca/signals.py`, conectada en `apps.py`), así ninguna vista tiene que acordarse de crearlo.
- `Socio.usuario` conecta una cuenta con su ficha de socio. Es opcional a propósito: un socio puede existir sin cuenta web (si el mesón lo registró pero la persona nunca inició sesión), y una cuenta puede existir sin ser socio (como `lector`, la cuenta de prueba genérica).
- `Comentario` es el foro: cada libro (`/libros/<id>/`) tiene su propia lista de opiniones y un formulario para agregar la propia, con el mismo patrón de validación en cliente y servidor que el resto del sitio (mínimo 5 caracteres).
