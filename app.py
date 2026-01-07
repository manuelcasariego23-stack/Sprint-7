import pandas as pd
import streamlit as st
import plotly.express as px

# ---------------------------
# Configuración de la página
# ---------------------------
st.set_page_config(
    page_title="Análisis del Mercado de Vehículos Usados en EE.UU",
    layout="wide"
)

st.title("Análisis Exploratorio del Mercado de Vehículos Usados en EE.UU")

st.markdown("""
Esta aplicación permite explorar y analizar el mercado de vehículos usados en EE.UU.
A través de visualizaciones interactivas, se estudian precios, kilometraje y características
clave que influyen en el valor de los vehículos.
""")

# ---------------------------
# Carga y limpieza de datos
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/vehicles_us.csv")

    df["model_year"] = df["model_year"].fillna(df["model_year"].median())
    df["cylinders"] = df["cylinders"].fillna(df["cylinders"].mode()[0])
    df["odometer"] = df["odometer"].fillna(df["odometer"].median())
    df["paint_color"] = df["paint_color"].fillna("unknown")
    df["is_4wd"] = df["is_4wd"].fillna(0)

    return df

df = load_data()

# ---------------------------
# Barra lateral (controles)
# ---------------------------
st.sidebar.header("🔎 Opciones de análisis")

analysis_option = st.sidebar.selectbox(
    "Selecciona una visualización",
    (
        "Distribución de precios",
        "Distribución del kilometraje",
        "Kilometraje vs Precio",
        "Precio promedio por tipo de vehículo",
        "Precio según condición",
        "Precio por tipo de combustible"
    )
)

# ---------------------------
# Visualizaciones
# ---------------------------

if analysis_option == "Distribución de precios":
    st.subheader("📊 Distribución de precios")

    st.markdown("""
    **Objetivo:** Analizar cómo se distribuyen los precios de los vehículos usados.
    
    **Insight esperado:**  
    La mayoría de los vehículos se concentran en rangos de precio bajos a medios,
    con una cola larga que representa vehículos de alto valor.
    """)

    fig = px.histogram(
        df,
        x="price",
        nbins=100,
        labels={"price": "Precio (USD)", "count": "Número de vehículos"},
        title="Distribución de precios de vehículos usados"
    )
    st.plotly_chart(fig, use_container_width=True)


elif analysis_option == "Distribución del kilometraje":
    st.subheader("📊 Distribución del kilometraje")

    st.markdown("""
    **Objetivo:** Evaluar el uso promedio de los vehículos según su kilometraje.
    
    **Insight esperado:**  
    Se observa una alta concentración de vehículos con kilometrajes elevados,
    lo cual es típico del mercado de autos usados.
    """)

    fig = px.histogram(
        df,
        x="odometer",
        nbins=80,
        labels={"odometer": "Kilometraje (millas)", "count": "Número de vehículos"},
        title="Distribución del kilometraje"
    )
    st.plotly_chart(fig, use_container_width=True)


elif analysis_option == "Kilometraje vs Precio":
    st.subheader("📉 Relación entre kilometraje y precio")

    st.markdown("""
    **Objetivo:** Analizar la relación entre el kilometraje y el precio.
    
    **Insight clave:**  
    Existe una relación inversa: a mayor kilometraje, menor precio,
    aunque el año del modelo introduce variabilidad en esta relación.
    """)

    fig = px.scatter(
        df,
        x="odometer",
        y="price",
        color="model_year",
        opacity=0.6,
        labels={
            "odometer": "Kilometraje (millas)",
            "price": "Precio (USD)",
            "model_year": "Año del modelo"
        },
        title="Kilometraje vs Precio por año del modelo"
    )
    st.plotly_chart(fig, use_container_width=True)


elif analysis_option == "Precio promedio por tipo de vehículo":
    st.subheader(" Precio promedio por tipo de vehículo")

    st.markdown("""
    **Objetivo:** Comparar el precio promedio según el tipo de vehículo.
    
    **Insight esperado:**  
    Camionetas y SUVs tienden a tener precios promedio más altos en comparación con sedanes y hatchbacks.
    """)

    avg_price_type = df.groupby("type", as_index=False)["price"].mean()

    fig = px.bar(
        avg_price_type,
        x="type",
        y="price",
        labels={"type": "Tipo de vehículo", "price": "Precio promedio (USD)"},
        title="Precio promedio por tipo de vehículo"
    )
    st.plotly_chart(fig, use_container_width=True)


elif analysis_option == "Precio según condición":
    st.subheader(" Precio según la condición del vehículo")

    st.markdown("""
    **Objetivo:** Analizar cómo influye la condición del vehículo en su precio.
    
    **Insight clave:**  
    Los vehículos en mejor condición presentan precios significativamente más altos,
    y con una dispersión menor.
    """)

    fig = px.box(
        df,
        x="condition",
        y="price",
        color="condition",
        labels={"condition": "Condición", "price": "Precio (USD)"},
        title="Precio según condición del vehículo"
    )
    st.plotly_chart(fig, use_container_width=True)


elif analysis_option == "Precio por tipo de combustible":
    st.subheader("Precio por tipo de combustible")

    st.markdown("""
    **Objetivo:** Comparar precios según el tipo de combustible.
    
    **Insight esperado:**  
    Vehículos eléctricos y diésel tienden a mostrar precios más altos
    en comparación con gasolina.
    """)

    fig = px.box(
        df,
        x="fuel",
        y="price",
        color="fuel",
        labels={"fuel": "Tipo de combustible", "price": "Precio (USD)"},
        title="Precio por tipo de combustible"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Cierre
# ---------------------------
st.markdown("---")
st.markdown(
    " **Proyecto desarrollado con Python, Pandas, Plotly y Streamlit.**"
)

    