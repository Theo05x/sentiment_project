import streamlit as st
import pandas as pd
from components.api import api_call
from components.charts import create_horizontal_bar

st.set_page_config(page_title="Análisis de Temas", page_icon="📋")

st.header("📋 Análisis de Temas")
st.markdown("Desglosa las menciones por subtema para entender mejor los problemas")

sentiment_filter = st.selectbox("Selecciona sentimiento a analizar",
                               ["negative", "positive", "neutral"],
                               format_func=lambda x: {"negative": "😞 Negativo", "positive": "😊 Positivo", "neutral": "😐 Neutral"}[x])

data = api_call("/metrics/topics", params={"sentiment": sentiment_filter})
if data and data.get("topics"):
    topics = data["topics"]
    
    col1, col2 = st.columns(2)
    
    # Gráfico de barras
    with col1:
        color_map = {
            "negative": "#e74c3c",
            "positive": "#2ecc71",
            "neutral": "#95a5a6"
        }
        fig = create_horizontal_bar(
            topics, 
            f"Subtemas - {sentiment_filter.upper()}",
            color=color_map.get(sentiment_filter, "#3498db")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla
    with col2:
        st.markdown("### Detalles por Tema")
        df_topics = pd.DataFrame(list(topics.items()), columns=["Tema", "Menciones"])
        df_topics = df_topics.sort_values("Menciones", ascending=False)
        df_topics["% del Total"] = (df_topics["Menciones"] / df_topics["Menciones"].sum() * 100).round(2)
        
        st.dataframe(df_topics, use_container_width=True, hide_index=True)
        
        # Insights
        st.markdown("### 💡 Insights")
        top_theme = df_topics.iloc[0]
        st.info(f"El tema principal es **{top_theme['Tema']}** con {top_theme['Menciones']} menciones ({top_theme['% del Total']:.1f}%)")
else:
    st.info("No hay datos de temas disponibles")
