import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Tuple, Optional

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

try:
    US_CITIES = pd.read_csv("app/data/usa_cities.csv")
    US_CITIES["city"] = US_CITIES["city"].astype(str).str.strip().str.lower()
except Exception:
    US_CITIES = pd.DataFrame(columns=["city","state","lat","lon"])

def get_city_coords(city: str) -> Optional[tuple]:
    if not isinstance(city, str):
        return None
    key = city.strip().lower()

    row = US_CITIES[US_CITIES["city"] == key]
    if not row.empty:
        return float(row.iloc[0]["lat"]), float(row.iloc[0]["lon"])
    for candidate in US_CITIES["city"].unique():
        if candidate in key:
            r = US_CITIES[US_CITIES["city"] == candidate]
            return float(r.iloc[0]["lat"]), float(r.iloc[0]["lon"])
    return None

def create_geo_map(df: pd.DataFrame, location_col: str = "Ubicación", count_col: str = "Menciones"):
  
    if df is None or df.empty:
        return None

    work = df.copy()
    work[location_col] = work[location_col].astype(str).str.strip().str.lower()

    work["coords"] = work[location_col].apply(get_city_coords)
    work = work.dropna(subset=["coords"])

    if work.empty:
        return None

    work["lat"] = work["coords"].apply(lambda x: x[0])
    work["lon"] = work["coords"].apply(lambda x: x[1])

    fig = px.scatter_geo(
        work,
        lat="lat",
        lon="lon",
        size=count_col,
        hover_name=location_col,
        text=location_col,    
        projection="natural earth",
        scope="north america",
        title="Localizaciones",
    )

    # 🎨 Mejoras visuales
    fig.update_traces(
        marker=dict(
            color="black",
            opacity=0.75,
            line=dict(width=1, color="white"),  
            sizemode="area"
        ),
        textposition="top center",
        textfont=dict(size=12, color="black")
    )

    fig.update_layout(
        height=650,
        margin=dict(r=0, t=50, l=0, b=0),
        geo=dict(
            showland=True,
            landcolor="#f5f5f5",
            showcountries=True,
            countrycolor="#888",
            showlakes=True,
            lakecolor="#d6e4ff",
            coastlinecolor="#555",
            bgcolor="rgba(0,0,0,0)", 
        ),
        title=dict(
            x=0.5,
            font=dict(size=20, color="#222", family="Arial")
        )
    )

    return fig
