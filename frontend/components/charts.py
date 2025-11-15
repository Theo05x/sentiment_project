"""
Componentes de gráficos reutilizables
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Tuple


def create_sentiment_pie(sentiments: Dict[str, int]) -> go.Figure:
    """Crea gráfico de dona de sentimiento"""
    fig = go.Figure(data=[go.Pie(
        labels=list(sentiments.keys()),
        values=list(sentiments.values()),
        hole=0.3,
        marker=dict(colors=['#2ecc71', '#95a5a6', '#e74c3c'])
    )])
    fig.update_layout(height=300, showlegend=True)
    return fig


def create_time_series_chart(data: List[Dict]) -> go.Figure:
    """Crea gráfico de líneas para series temporales"""
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['period'], y=df['positive'], name='Positivo', line=dict(color='#2ecc71')))
    fig.add_trace(go.Scatter(x=df['period'], y=df['neutral'], name='Neutral', line=dict(color='#95a5a6')))
    fig.add_trace(go.Scatter(x=df['period'], y=df['negative'], name='Negativo', line=dict(color='#e74c3c')))
    
    fig.update_layout(
        title="Tendencia de Sentimiento",
        xaxis_title="Período",
        yaxis_title="Cantidad de Menciones",
        hovermode='x unified',
        height=500
    )
    return fig


def create_horizontal_bar(data: Dict[str, int], title: str, color: str = '#3498db', max_items: int = 20) -> go.Figure:
    """Crea gráfico de barras horizontal"""
    items = dict(list(data.items())[:max_items])
    
    fig = go.Figure([go.Bar(
        x=list(items.values()),
        y=list(items.keys()),
        orientation='h',
        marker=dict(color=color)
    )])
    fig.update_layout(
        title=title,
        xaxis_title="Cantidad",
        height=500
    )
    return fig


def create_keywords_bar(keywords: List[Tuple[str, int]], max_items: int = 20) -> go.Figure:
    """Crea gráfico de barras para palabras clave"""
    keywords_dict = dict(keywords[:max_items])
    
    fig = go.Figure([go.Bar(
        x=list(keywords_dict.values()),
        y=list(keywords_dict.keys()),
        orientation='h',
        marker=dict(color='#3498db')
    )])
    fig.update_layout(
        title=f"Top {min(max_items, len(keywords))} Palabras",
        xaxis_title="Frecuencia",
        height=500
    )
    return fig


def create_influencers_chart(df: pd.DataFrame, max_items: int = 20) -> go.Figure:
    """Crea gráfico para influencers"""
    df = df.head(max_items)
    
    fig = go.Figure([go.Bar(
        x=df['count'],
        y=df['name'],
        orientation='h',
        marker=dict(
            color=df['retweets'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Retweets")
        )
    )])
    fig.update_layout(
        title=f"Top {len(df)} Influencers",
        xaxis_title="Cantidad de Menciones",
        yaxis_title="Usuario",
        height=500
    )
    return fig


def create_geo_chart(df: pd.DataFrame, max_items: int = 20) -> go.Figure:
    """Crea gráfico para análisis geográfico"""
    df = df.head(max_items)
    
    fig = go.Figure([go.Bar(
        y=df['location'],
        x=df['count'],
        orientation='h',
        marker=dict(color='#9b59b6')
    )])
    fig.update_layout(
        title=f"Top {len(df)} Ubicaciones Geográficas",
        xaxis_title="Cantidad de Menciones",
        yaxis_title="Ubicación",
        height=500
    )
    return fig
