import streamlit as st
import pandas as pd
from components.api import api_call
from components.charts import create_sentiment_pie
from components.ui import render_metrics

st.set_page_config(page_title="Resumen", page_icon="📊")

st.header("📊 Resumen de Sentimiento")
st.markdown("Proporciones y KPI de sentimiento general")

data = api_call("/metrics/summary")
if data:
    total = data.get("total_tweets", 0)
    sentiments = data.get("by_sentiment", {})
    avg_score = data.get("avg_score", 0)
    
    # Métricas principales
    render_metrics(
        total=total,
        positive=sentiments.get('positive', 0),
        neutral=sentiments.get('neutral', 0),
        negative=sentiments.get('negative', 0),
        avg_score=avg_score
    )
    
    # Gráfico de dona
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Distribución de Sentimiento")
        fig = create_sentiment_pie(sentiments)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Detalles")
        df = pd.DataFrame([sentiments]).T.reset_index()
        df.columns = ["Sentimiento", "Cantidad"]
        df["Porcentaje"] = (df["Cantidad"] / total * 100).round(2)
        st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No hay datos disponibles. Sube un CSV primero.")
