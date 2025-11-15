"""
Componentes de UI reutilizables
"""
import streamlit as st
from components.api import recompute_cache, ingest_csv, predict_sentiment


def render_sidebar():
    """Renderiza la barra lateral con controles"""
    with st.sidebar:
        st.header("⚙️ Controles")
        
        # Botón para recargar datos
        if st.button("🔄 Recargar datos (limpiar caché)", use_container_width=True):
            if recompute_cache():
                st.success("✅ Caché limpiado")
                st.rerun()
            else:
                st.error("Error al limpiar caché")
        
        st.markdown("---")
        
        # Sección de importar datos
        st.subheader("📁 Importar datos")
        uploaded_file = st.file_uploader("Selecciona un CSV", type=["csv"])
        if uploaded_file is not None:
            with st.spinner("Subiendo archivo..."):
                result = ingest_csv(uploaded_file)
                if result:
                    st.success(f"✅ {result['rows_loaded']} filas importadas")
                    recompute_cache()
                    st.rerun()
        
        st.markdown("---")
        
        # Predicción rápida
        st.subheader("🔮 Predicción Rápida")
        test_text = st.text_input("Escribe un texto para predecir sentimiento:", 
                                  value="I love this product!",
                                  placeholder="Ej: Great service!")
        if st.button("Predecir", use_container_width=True):
            pred = predict_sentiment(test_text)
            if pred:
                sentiment = pred['label']
                score = pred['score']
                emoji = "😊" if sentiment == "positive" else "😐" if sentiment == "neutral" else "😞"
                st.info(f"{emoji} {sentiment.upper()}\nScore: {score:.2f}")


def render_header():
    """Renderiza el encabezado principal"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Panel de Análisis de Sentimiento")
        st.markdown("Monitorea menciones de marca en redes sociales y analiza el sentimiento público")
    with col2:
        from components.api import check_backend_health
        if check_backend_health():
            st.markdown("### ✅ Backend Online")
        else:
            st.markdown("### ❌ Backend Offline")
            st.warning("El servidor FastAPI no está disponible")
    
    st.markdown("---")


def render_footer():
    """Renderiza el pie de página"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; font-size: 0.9rem; padding: 1rem;">
        <p>Panel de Análisis de Sentimiento | Noviembre 2025</p>
        <p>📖 <a href="http://127.0.0.1:8000/docs" target="_blank">API Docs</a> | 
           💻 <a href="https://streamlit.io/" target="_blank">Streamlit</a> | 
           ⚡ <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a></p>
    </div>
    """, unsafe_allow_html=True)


def render_metrics(total: int, positive: int, neutral: int, negative: int, avg_score: float):
    """Renderiza métricas principales"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total de Tweets", f"{total:,}")
    with col2:
        st.metric("😊 Positivos", f"{positive:,}", 
                 delta=f"{(positive/total*100):.1f}%" if total > 0 else "0%")
    with col3:
        st.metric("😐 Neutrales", f"{neutral:,}",
                 delta=f"{(neutral/total*100):.1f}%" if total > 0 else "0%")
    with col4:
        st.metric("😞 Negativos", f"{negative:,}",
                 delta=f"{(negative/total*100):.1f}%" if total > 0 else "0%")
    
    st.markdown("---")
    
    # Score promedio
    col1, col2 = st.columns([2, 1])
    with col1:
        st.metric("🎯 Score Promedio de Sentimiento", f"{avg_score:.3f}", 
                 help="Rango: -1 (muy negativo) a +1 (muy positivo)")
    
    # Interpretación
    if avg_score > 0.3:
        st.success("✅ Sentimiento general POSITIVO")
    elif avg_score < -0.3:
        st.error("❌ Sentimiento general NEGATIVO")
    else:
        st.info("⚪ Sentimiento general NEUTRAL")
