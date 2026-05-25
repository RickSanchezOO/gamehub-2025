Cómo ejecutar las pruebas del backend
=====================================

Resumen rápido
--------------
Los tests del backend están en `GameHub-Backend/tests`. Para ejecutar la
suite completa usa `pytest` desde la raíz del proyecto o desde la carpeta
`GameHub-Backend`.

Comandos
--------
```powershell
# Desde la raíz del repo (usa el intérprete del entorno):
python -m pytest -q

# O especificando el intérprete detectado en este entorno:
C:\Users\ASUS\AppData\Local\spyder-6\envs\spyder-runtime\python.exe -m pytest -q
```

Notas
-----
- La configuración de pruebas usa SQLite en memoria para asegurar aislamiento.
- Se actualizó `GameHub-Backend/config.py` para usar SQLite como fallback
  si no se especifica una configuración MySQL completa.
- Se muestran advertencias sobre deprecaciones pero las pruebas pasan.
