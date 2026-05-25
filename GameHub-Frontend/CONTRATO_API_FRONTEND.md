# Contrato API Frontend Game-Hub

Documento de apoyo para conectar el frontend actual con el backend Python y la BD MySQL declarados en la Fase 1.

## Objetivo

Permitir que el frontend pueda desarrollarse antes de tener el backend completo, dejando claras las rutas, los datos esperados y el comportamiento minimo de cada modulo.

## Modulos principales

- Autenticacion y usuarios
- Catalogo y ranking de videojuegos
- Noticias
- Blog de opinion y comentarios
- Multimedia
- Agenda de eventos
- Equipo editorial
- Contacto
- Dashboard

## Endpoints sugeridos

### Autenticacion

- `POST /api/auth/register`
  - body:
    ```json
    {
      "displayName": "Daniel",
      "email": "daniel@example.com",
      "password": "******"
    }
    ```
  - response:
    ```json
    {
      "message": "Usuario registrado correctamente",
      "user": {
        "id": 1,
        "displayName": "Daniel",
        "role": "subscriber"
      }
    }
    ```

- `POST /api/auth/login`
  - body:
    ```json
    {
      "email": "daniel@example.com",
      "password": "******"
    }
    ```
  - response:
    ```json
    {
      "token": "jwt-o-token-equivalente",
      "user": {
        "id": 1,
        "displayName": "Daniel",
        "role": "subscriber"
      }
    }
    ```

### Catalogo

- `GET /api/games`
- `GET /api/games/:id`
- `GET /api/games/ranking`

Respuesta sugerida:

```json
[
  {
    "id": 1,
    "title": "Elden Ring",
    "genre": "Action RPG",
    "platform": "PC / Consolas",
    "description": "Mundo abierto oscuro...",
    "pressScore": 96,
    "communityScore": 93
  }
]
```

### Noticias

- `GET /api/news`
- `GET /api/news/:id`
- `POST /api/news`
- `PUT /api/news/:id`

Respuesta sugerida:

```json
[
  {
    "id": 10,
    "title": "La IA generativa entra en pipelines de arte y QA",
    "category": "Tecnologia",
    "excerpt": "Los estudios la usan para prototipado rapido...",
    "author": "Daniel Rovira",
    "date": "2026-05-16",
    "status": "published"
  }
]
```

### Blog y comentarios

- `GET /api/posts`
- `GET /api/posts/:id`
- `GET /api/posts/:id/comments`
- `POST /api/posts/:id/comments`

Comentario sugerido:

```json
{
  "id": 200,
  "author": "Usuario",
  "body": "Muy buen articulo",
  "status": "published",
  "createdAt": "2026-05-18T18:30:00"
}
```

### Multimedia

- `GET /api/media`

### Agenda

- `GET /api/events`

### Equipo editorial

- `GET /api/team`

### Contacto

- `POST /api/contact`

### Dashboard

- `GET /api/dashboard`

Respuesta sugerida:

```json
{
  "welcome": "Bienvenido de nuevo a tu panel.",
  "stats": [
    { "label": "Comentarios publicados", "value": 24 },
    { "label": "Noticias guardadas", "value": 7 },
    { "label": "Eventos seguidos", "value": 5 }
  ]
}
```

## Reglas de integracion

- El frontend actual usa datos mock en `assets/js/data.js`.
- Cada bloque visual puede sustituirse por `fetch()` a la ruta correspondiente.
- Los formularios de `auth.html` y `contacto.html` estan preparados para conectar con backend real.
- El dashboard deberia requerir sesion iniciada y rol valido.
- Las rutas de creacion o modificacion de contenido deben comprobar permisos por rol.

## Prioridad de conexion real

1. `auth.html`
2. `dashboard.html`
3. `noticias.html`
4. `blog.html`
5. `catalogo.html`
6. `contacto.html`

## Beneficio para la entrega

Este contrato permite justificar que el frontend se ha implementado de forma desacoplada pero coherente con el backend y la base de datos definidos en la planificacion del proyecto.
