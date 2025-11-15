import streamlit as st
from components.ui import render_sidebar, render_header, render_footer

# Configuración de la página
st.set_page_config(
    page_title="Sentiment Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main { padding: 2rem; }
    .metric-card { 
        background-color: #f0f2f6; 
        padding: 1.5rem; 
        border-radius: 0.5rem; 
        margin: 1rem 0;
    }
    h1 { color: #1f77b4; }
    h2 { color: #ff7f0e; }
</style>
""", unsafe_allow_html=True)

# Renderizar componentes
render_header()
render_sidebar()

st.markdown("""
## 🎯 Bienvenido al Panel de Análisis de Sentimiento

Utiliza el menú lateral para:
- **Importar datos**: Sube un archivo CSV con datos de menciones
- **Predecir**: Analiza el sentimiento de textos individuales
- **Recargar**: Limpia el caché después de importar datos

## 📊 Vistas Disponibles

En el panel principal encontrarás 6 análisis completos:

1. **📊 Resumen** - Proporciones de sentimiento y KPIs
2. **📈 Evolución Temporal** - Tendencias a lo largo del tiempo
3. **☁️ Palabras Clave** - Nube de palabras interactiva
4. **📋 Análisis de Temas** - Desglose por subtemas
5. **👥 Influencers** - Usuarios con mayor impacto
6. **🗺️ Análisis Geográfico** - Distribución por ubicación

## 🚀 Primeros Pasos

1. Haz clic en "📁 Importar datos" en el sidebar
2. Selecciona un archivo CSV con columnas: `text`, `airline_sentiment`, `tweet_created`, `name`, `retweet_count`, `tweet_location`
3. Una vez importado, navega a cualquiera de las 6 vistas para explorar los datos

""")

render_footer()

