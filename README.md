🎮 GAME-HUB & SERVICES ECOSYSTEM

Este repositorio contiene el código fuente completo y el entorno de pruebas automatizadas de la plataforma web GameHub, desarrollado para la asignatura de Gestión de Proyectos de Ingeniería de Software (GPIS).

👥 Equipo de Desarrollo:
Daniel Rovira — Project Manager / Coordinador de Gestión
Ricardo Sánchez — Backend Developer / SCM Manager
Francisco Federico García — Testing Engineer / Quality Assurance
Alejandro Álvarez — Data Architect / Software Analyst

📂 Estructura General del Proyecto:
📁 GameHub-Backend/ → Servidor backend y API desarrollados en Python + Flask.
📁 GameHub-Frontend/ → Interfaz visual web y recursos del cliente.
📁 tests/ → Entorno automatizado de pruebas QA con pytest.
📄 requirements.txt → Dependencias necesarias para ejecutar el proyecto.

🚀 Guía Rápida de Instalación y Ejecución
1️⃣ Instalar Dependencias

Abra una terminal (cmd o PowerShell), acceda al backend e instale todas las dependencias necesarias:

cd GameHub-Backend
pip install -r requirements.txt

2️⃣ Ejecutar las Pruebas QA

Para comprobar el correcto funcionamiento del sistema:

pytest

3️⃣ Iniciar el Servidor

Ejecute el servidor Flask principal:

python run.py

La aplicación quedará disponible en:

http://127.0.0.1:5000

⚠️ No cierre la terminal mientras el servidor esté en ejecución.

4️⃣ Acceder a la Plataforma

Abra su navegador web e introduzca la siguiente URL:

http://127.0.0.1:5000/frontend

La interfaz web de GameHub se cargará automáticamente conectada al backend integrado.
