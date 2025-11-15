import streamlit as st
import pandas as pd
from components.api import api_call
from components.charts import create_influencers_chart

st.set_page_config(page_title="Influencers", page_icon="👥")

st.header("👥 Identificación de Influencers y Detractores")
st.markdown("Identifica usuarios con mayor impacto en las menciones")

col1, col2, col3 = st.columns(3)
with col1:
    sentiment = st.selectbox("Filtrar por sentimiento",
                            [None, "positive", "negative", "neutral"],
                            format_func=lambda x: "Sin filtro" if x is None else {"positive": "Positivo", "negative": "Negativo", "neutral": "Neutral"}[x],
                            key="inf_sentiment")
with col2:
    limit = st.slider("Mostrar top N", 5, 50, 20, key="inf_limit")
with col3:
    sort_by = st.selectbox("Ordenar por", ["count", "retweets"],
                          format_func=lambda x: "Cantidad de Menciones" if x == "count" else "Retweets")

data = api_call("/metrics/influencers", 
               params={"sentiment": sentiment, "limit": limit, "sort_by": sort_by})
if data and data.get("influencers"):
    influencers = data["influencers"]
    df = pd.DataFrame(influencers)
    
    # Gráfico
    fig = create_influencers_chart(df, max_items=limit)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla detallada
    st.subheader("📊 Detalles")
    df_display = df.copy()
    df_display.columns = ["Usuario", "Menciones", "Retweets"]
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Estadísticas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Usuarios", len(df))
    with col2:
        st.metric("Menciones Totales", df['count'].sum())
    with col3:
        st.metric("Retweets Totales", df['retweets'].sum())
else:
    st.info("No hay datos de influencers disponibles")
