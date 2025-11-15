import streamlit as st
import pandas as pd
from components.api import api_call
from components.charts import create_time_series_chart

st.set_page_config(page_title="Evolución Temporal", page_icon="📈")

st.header("📈 Evolución del Sentimiento en el Tiempo")
st.markdown("Observa cómo ha cambiado el sentimiento a lo largo del período")

col1, col2 = st.columns(2)
with col1:
    freq = st.selectbox("Granularidad", ["D", "W", "M"], 
                       format_func=lambda x: {"D": "Diario", "W": "Semanal", "M": "Mensual"}[x],
                       help="D=Diario, W=Semanal, M=Mensual")

data = api_call("/metrics/time_series", params={"freq": freq})
if data and len(data) > 0:
    # Gráfico de líneas
    fig = create_time_series_chart(data)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de datos
    with st.expander("Ver datos de la tabla"):
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    
    # Estadísticas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Períodos", len(data))
    with col2:
        st.metric("Max Positivos", max([d.get('positive', 0) for d in data]))
    with col3:
        st.metric("Max Negativos", max([d.get('negative', 0) for d in data]))
else:
    st.info("No hay datos disponibles para mostrar la evolución temporal")
