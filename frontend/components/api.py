"""
Módulo para manejar llamadas a la API del backend
"""
import requests
import streamlit as st
from typing import Optional, Dict, Any

API_URL = "https://sentiment-backend-xxxx.onrender.com/api/v1"  # Reemplaza xxxx con tu URL de Render
HEALTH_URL = "https://sentiment-backend-xxxx.onrender.com/health"


def check_backend_health() -> bool:
    """Verifica si el backend está disponible"""
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        return response.status_code == 200
    except:
        return False


def api_call(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
    """
    Realiza llamada a la API y maneja errores
    
    Args:
        endpoint: Ruta del endpoint (ej: "/metrics/summary")
        params: Parámetros de query
        
    Returns:
        Respuesta JSON o None si hay error
    """
    try:
        url = f"{API_URL}{endpoint}"
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ No se puede conectar al backend. Asegúrate de que FastAPI está corriendo en http://127.0.0.1:8000")
        return None
    except Exception as e:
        st.error(f"❌ Error en la solicitud: {str(e)}")
        return None


def predict_sentiment(text: str) -> Optional[Dict]:
    """Predice sentimiento para un texto"""
    try:
        response = requests.post(f"{API_URL}/predict/predict", 
                                json={"text": text}, 
                                timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error: {str(e)}")
    return None


def recompute_cache() -> bool:
    """Limpia el caché del backend"""
    try:
        requests.post(f"{API_URL}/metrics/recompute", timeout=10)
        return True
    except:
        return False


def ingest_csv(file) -> Optional[Dict]:
    """Sube un archivo CSV al backend"""
    try:
        files = {"file": file}
        response = requests.post(f"{API_URL}/ingest/ingest_csv", files=files, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error al subir: {str(e)}")
    return None
