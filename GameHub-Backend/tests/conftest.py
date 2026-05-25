"""
Fixtures de Pytest para el backend de GameHub.

Este módulo define dos fixtures principales:
- `app`: crea la aplicación Flask en modo `TESTING` y monta
    una base de datos en memoria (`sqlite:///:memory:`) para pruebas.
- `client`: devuelve un cliente de prueba (Flask test_client)
    ligado a la aplicación creada por `app`.

Notas:
- La base de datos en memoria se crea antes de cada sesión de prueba
    y se destruye al finalizar para asegurar aislamiento entre tests.
"""

import pytest
from app import create_app, db


@pytest.fixture
def app():
        # Crear la aplicación con configuración específica para pruebas
        app = create_app()
        app.config.update({
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
                "SECRET_KEY": "test-secret-key",
                "WTF_CSRF_ENABLED": False,
        })

        # Contexto de aplicación: crea todas las tablas antes de ceder la app
        with app.app_context():
                db.create_all()
                yield app
                # Limpieza: cerrar sesión y eliminar tablas
                db.session.remove()
                db.drop_all()


@pytest.fixture
def client(app):
        """Cliente de pruebas para realizar peticiones HTTP dentro de tests."""
        return app.test_client()
