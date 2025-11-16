import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Análisis del Mercado de vehiculos usados en EE.UU",
    layout="wide")

st.header(" Análisis Exploratorio de Vehículos Usados")
st.write("""
Ayudate de esta applicacion para explorar y analizar el mercado de vehículos usados en EE.UU.
puedes analizar la distribución de precios, kilometraje y características mediante los gráficos interactivos.
Usa los botones para generar las visualizaciones.
""")

@st.cache_data
def load_data():
    df = pd.read_csv("data/vehicles_us.csv")
    df['model_year'] = df['model_year'].fillna(df['model_year'].median())
    df['cylinders'] = df['cylinders'].fillna(df['cylinders'].mode()[0])
    df['odometer'] = df['odometer'].fillna(df['odometer'].median())
    df['paint_color'] = df['paint_color'].fillna('unknown')
    df['is_4wd'] = df['is_4wd'].fillna(0)
    return df

df = load_data()

if st.button("Mostrar histograma del precio"):
    st.write("Distribución del precio de los vehículos")
    fig_hist = px.histogram(
        df,
        x="price",
        nbins=100,
        title="Distribución de precios",
        labels={"price": "Precio (USD)", "count": "Número de vehículos"},
        color_discrete_sequence=["#0072B2"])
    st.plotly_chart(fig_hist, use_container_width=True)

    #Botón 2: Gráfico de dispersión 
if st.button("Mostrar gráfico de dispersión (Kilometraje vs Precio)"):
    st.write("Relación entre kilometraje y precio")
    fig_scatter = px.scatter(
        df,
        x="odometer",
        y="price",
        color="fuel",
        title="Kilometraje vs Precio por tipo de combustible",
        labels={"odometer": "Kilometraje (millas)", "price": "Precio (USD)", "fuel": "Tipo de combustible"},
        hover_data=["model_year", "type"])
    st.plotly_chart(fig_scatter, use_container_width=True)

    