# StudentOverflow 🎓

StudentOverflow es un proyecto tipo foro/preguntas-respuestas inspirado en plataformas como StackOverflow, pensado para estudiantes de Hybridge.
La aplicación utiliza **Flask** como backend, conexión con **Supabase** como base de datos, y soporta registro/login de usuarios, asi como almacena todos los datos del usuario, ya sea admin o estudiante, los cuales son el nombre, correo, contraseña y el rol, asi como todas las preguntas que ha hecho o comentarios que ha agregado recientemente en la plataforma.

---

## 🚀 Tecnologías utilizadas

- **Flask** → Framework web en Python para levantar el servidor y manejar las rutas.  
- **python-dotenv** → Para cargar y manejar las variables de entorno desde un archivo `.env`.  
- **Supabase** → Base de datos en la nube (PostgreSQL) con uso de la API y sus API KEY para interactuar fácilmente.  
- **SQLAlchemy** → ORM que permite interactuar con bases de datos SQL de forma sencilla.  
- **psycopg2-binary** → Driver para conectar Python con PostgreSQL.  

---

## ⚙️ Creación del entorno virtual de Python

```bash
python -m venv .venv
source .venv/bin/activate   # En Linux/Mac
.venv\Scripts\activate      # En Windows
```

---

### 💻 Instalación de dependencias
```bash
pip install -r requirements.txt
```





