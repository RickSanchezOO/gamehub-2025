Resumen de tests y cambios realizados
=====================================

Objetivo
-------
Documentar y comentar los cambios realizados para permitir pruebas unitarias
e integradas del backend GameHub.

Cambios principales
-------------------
- Añadidos tests unitarios e integrales en `GameHub-Backend/tests`:
  - `conftest.py` (fixtures)
  - `test_models.py` (tests de modelos)
  - `test_api.py` (tests de endpoints REST)
- Actualizado `GameHub-Backend/config.py` para permitir un fallback a SQLite
  cuando las variables de entorno MySQL no estén definidas. Esto evita
  errores de arranque y facilita ejecutar las pruebas localmente.
- Añadido `pytest.ini` en la raíz para que Pytest detecte la carpeta de tests
  aunque se ejecute desde la raíz del proyecto.

Por qué fue necesario
---------------------
El proyecto original requería variables de entorno para construir la URI de
conexión a MySQL; al no estar presentes provocaba errores de parsing en
SQLAlchemy durante la inicialización. Para pruebas locales y CI se usa SQLite
en memoria o un archivo local como fallback.

Cómo ejecutar las pruebas
-------------------------
Desde la raíz del proyecto (usa el intérprete del entorno indicado):

```powershell
# Si usas el intérprete que configuré en este entorno:
C:\Users\ASUS\AppData\Local\spyder-6\envs\spyder-runtime\python.exe -m pytest -q

# O simplemente, si tu PATH está configurado para el entorno:
python -m pytest -q
```

Resultados esperados
--------------------
- `9 passed` (como verificado durante la ejecución)
- Advertencias (warnings) relativas a deprecaciones de dependencias
  (por ejemplo `datetime.utcnow()` y `Query.get()`), que no impiden
  el correcto funcionamiento de las pruebas.

Siguientes pasos recomendados
----------------------------
- Opcional: corregir las advertencias deprecations (recomiendo:
  - usar `datetime.now(timezone.utc)` para fechas con zona horaria
  - reemplazar `Model.query.get(id)` por `db.session.get(Model, id)`)
- Añadir un `requirements.txt` o `pyproject.toml` para fijar versiones
  de dependencias y facilitar reproducibilidad.

Archivos relevantes
------------------
- `GameHub-Backend/config.py` (modificado)
- `GameHub-Backend/tests/*` (añadidos)
- `pytest.ini` (añadido en la raíz)

Contacto
--------
Si quieres que deje todo listo para CI (GitHub Actions) o que aplique las
correcciones para eliminar warnings, dímelo y lo implemento.
