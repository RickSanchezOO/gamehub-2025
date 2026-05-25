from app import create_app, db

# Creamos la instancia de la aplicación usando la factoría
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Crea todas las tablas en la base de datos si no existen
        # En producción esto se haría con migraciones (Flask-Migrate)
        db.create_all()
    
    # Arranca el servidor en modo debug
    # debug=True recarga automáticamente al detectar cambios en el código
    # IMPORTANTE: nunca usar debug=True en producción
    app.run(debug=True)