# Sentiment Analysis Dashboard - Análisis de Sentimiento en Redes Sociales

Herramienta de análisis de sentimiento para monitorear menciones de marca en redes sociales, medir sentimiento público e impacto de campañas.

## Requisitos

- Python 3.10+
- pip

## Instalación

1. **Clonar o descargar el proyecto:**
```bash
cd sentiment_project_v1
```

2. **Crear entorno virtual (opcional pero recomendado):**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
pip install streamlit plotly wordcloud
```

## Estructura del Proyecto

```
sentiment_project_v1/
├── app/
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuración
│   ├── api/
│   │   ├── routes.py           # Agregador de rutas
│   │   └── v1/
│   │       ├── predict.py      # Endpoint predicción
│   │       ├── ingest.py       # Endpoint ingest CSV
│   │       └── metrics.py      # Endpoints de agregaciones
│   ├── core/
│   │   ├── model.py            # Carga modelo
│   │   └── preprocess.py       # Preprocesamiento
│   ├── services/
│   │   ├── sentiment_service.py
│   │   ├── ingest_service.py
│   │   └── metrics_service.py
│   ├── schemas/
│   │   └── pydantic_schemas.py
│   └── data/                   # CSV guardados
├── frontend/
│   └── app.py                  # Streamlit principal
├── scripts/
│   └── run_dev.ps1            # Script desarrollo
└── requirements.txt
```

## Ejecución

### Opción 1: Lanzar por separado

**Terminal 1 - Backend:**
```bash
py -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
streamlit run frontend/app.py
```

### Opción 2: Script automático (Windows)
```powershell
.\scripts\run_dev.ps1
```

## API Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Verificar estado |
| `/api/v1/predict/predict` | POST | Predecir sentimiento |
| `/api/v1/ingest/ingest_csv` | POST | Subir CSV |
| `/api/v1/metrics/summary` | GET | Resumen sentimiento |
| `/api/v1/metrics/time_series` | GET | Series temporales |
| `/api/v1/metrics/keywords` | GET | Palabras clave |
| `/api/v1/metrics/topics` | GET | Análisis de temas |
| `/api/v1/metrics/influencers` | GET | Top influencers |
| `/api/v1/metrics/geo` | GET | Análisis geográfico |

## Dashboard (Streamlit)

6 vistas interactivas:
1. 📊 Resumen de Sentimiento
2. 📈 Evolución Temporal
3. ☁️ Palabras Clave
4. 📋 Análisis de Temas
5. 👥 Influencers
6. 🗺️ Análisis Geográfico

## Documentación Completa de API

Para ver todos los parámetros y ejemplos de cada endpoint, consulta la sección "API Endpoints" en este mismo documento o accede a la documentación interactiva en:

```
http://127.0.0.1:8000/docs
```

## Troubleshooting

- **Error "python-multipart not installed"**: `pip install python-multipart`
- **Error "Streamlit not installed"**: `pip install streamlit plotly wordcloud`
- **Backend no responde**: Verifica que uvicorn está corriendo en `:8000`
- **No hay datos**: Sube CSV con `/api/v1/ingest/ingest_csv` y llama a `/api/v1/metrics/recompute`

