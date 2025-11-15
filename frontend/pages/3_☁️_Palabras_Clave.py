import streamlit as st
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from components.api import api_call
from components.charts import create_keywords_bar

st.set_page_config(page_title="Palabras Clave", page_icon="☁️")

st.header("☁️ Nube de Palabras Clave")
st.markdown("Identifica rápidamente los temas principales de conversación")

col1, col2 = st.columns(2)
with col1:
    sentiment = st.selectbox("Filtrar por sentimiento", 
                            [None, "positive", "negative", "neutral"],
                            format_func=lambda x: "Sin filtro" if x is None else {"positive": "Positivo", "negative": "Negativo", "neutral": "Neutral"}[x])
with col2:
    top_n = st.slider("Top palabras", 10, 100, 50)

data = api_call("/metrics/keywords", params={"sentiment": sentiment, "top": top_n})
if data and data.get("keywords"):
    keywords = data["keywords"]
    
    # Gráfico de barras (top 20)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = create_keywords_bar(keywords, max_items=20)
        st.plotly_chart(fig, use_container_width=True)
    
    # WordCloud
    with col2:
        st.markdown("### Nube Interactiva")
        try:
            word_freq = dict(keywords)
            if word_freq:
                wordcloud = WordCloud(width=600, height=500, background_color='white').generate_from_frequencies(word_freq)
                fig, ax = plt.subplots(figsize=(10, 8))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
        except Exception as e:
            st.warning(f"No se pudo generar la nube de palabras: {str(e)}")
    
    # Tabla completa
    with st.expander("Ver todas las palabras clave"):
        df = pd.DataFrame(keywords, columns=["Palabra", "Frecuencia"])
        st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No hay palabras clave disponibles")
