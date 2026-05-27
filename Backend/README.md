# Gestión Profesoral Pro

## Qué incluye
- Backend FastAPI organizado por módulos y con rutas versionadas
- Frontend Flask tipo panel administrativo
- Base de datos PostgreSQL con claves foráneas
- Documentación automática en `/docs` y `/redoc`

## Cómo ejecutar

### 1. Configura PostgreSQL
Crea la base de datos `gestion_profesoral` y ejecuta `database/db.sql`.

### 2. Ejecuta el backend
Desde la raíz del proyecto:
```bash
python -m pip install -r api/requirements.txt
```

Windows PowerShell:
```powershell
$env:DATABASE_URL="postgresql+psycopg2://postgres:TU_PASSWORD@localhost:5432/gestion_profesoral"
python -m uvicorn api.app.main:app --reload
```

Linux / macOS:
```bash
export DATABASE_URL="postgresql+psycopg2://postgres:TU_PASSWORD@localhost:5432/gestion_profesoral"
python -m uvicorn api.app.main:app --reload
```

### 3. Ejecuta el frontend
En otra terminal:
```bash
python -m pip install -r front/requirements.txt
python front/app.py
```

## Puntos de navegación
- Frontend: `http://127.0.0.1:5000`
- API: `http://127.0.0.1:8000`
- Documentación: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`


#Backend
$env:PYTHONPATH = "."
python api/app/main.py
python api/app/main.py