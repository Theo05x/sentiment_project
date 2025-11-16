import streamlit as st
import pandas as pd
from components.api import api_call
from components.charts import create_geo_chart
from components.charts import create_geo_map

st.set_page_config(page_title="Análisis Geográfico", page_icon="🗺️")

st.header("🗺️ Análisis Geográfico de Menciones")
st.markdown("Visualiza de dónde provienen las menciones geográficamente")

top_n = st.slider("Mostrar top ubicaciones", 10, 100, 50, key="geo_top")


data = api_call("/metrics/geo", params={"top": top_n})
if data and data.get("geo"):
    geo_data = data["geo"]
    df = pd.DataFrame(geo_data)
    
    # Gráfico de barras
    fig = create_geo_chart(df, max_items=20)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla completa
    st.subheader(f"📍 Top {top_n} Ubicaciones")
    df_display = df.copy()
    df_display.columns = ["Ubicación", "Menciones"]
    df_display["% del Total"] = (df_display["Menciones"] / df_display["Menciones"].sum() * 100).round(2)
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Estadísticas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Ubicaciones", len(df))
    with col2:
        st.metric("Ubicación Top", df_display.iloc[0]["Ubicación"])
    with col3:
        st.metric("Menciones Top", df_display.iloc[0]["Menciones"])
else:
    st.info("No hay datos geográficos disponibles")
    
st.subheader("🌍 Mapa geográfico de menciones")

fig = create_geo_map(df_display)

if fig:
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No se pudo generar el mapa. Asegúrate de que el CSV tenga columnas lat, lon, Ubicación y Menciones.")
