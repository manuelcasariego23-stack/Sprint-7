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

st.title("Mercado de Vehículos Usados en EE.UU.")
st.caption("Dashboard interactivo de análisis exploratorio de datos")

st.markdown("""
Este dashboard permite explorar el mercado de vehículos usados en EE.UU.
mediante filtros y visualizaciones interactivas, con el objetivo de identificar
patrones en precios, kilometraje y características clave.
""")
st.markdown("---")
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
st.markdown("---")
# ---------------------------
# Barra lateral (controles)
# ---------------------------
st.sidebar.header(" Filtros")

vehicle_type = st.sidebar.multiselect(
    "Tipo de vehículo",
    options=sorted(df["type"].dropna().unique()),
    default=sorted(df["type"].dropna().unique())
)

fuel_type = st.sidebar.multiselect(
    "Tipo de combustible",
    options=sorted(df["fuel"].dropna().unique()),
    default=sorted(df["fuel"].dropna().unique())
)

price_range = st.sidebar.slider(
    "Rango de precios (USD)",
    int(df["price"].min()),
    int(df["price"].quantile(0.95)),
    (int(df["price"].min()), int(df["price"].quantile(0.95)))
)

df_filtered = df[
    (df["type"].isin(vehicle_type)) &
    (df["fuel"].isin(fuel_type)) &
    (df["price"].between(price_range[0], price_range[1]))
]

analysis_option = st.sidebar.radio(
    "Selecciona un análisis",
    [
        "Distribución de precios",
        "Distribución del kilometraje",
        "Kilometraje vs Precio",
        "Precio promedio por tipo de vehículo",
        "Precio según condición",
        "Precio por tipo de combustible",
        "Mapa de calor de correlaciones"
    ]
)
if df_filtered.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()
st.markdown("---")
# ---------------------------
# Visualizaciones
# ---------------------------

if analysis_option == "Distribución de precios":
    st.subheader("Distribución de precios")

    st.markdown("""
    **Insight esperado:**  
    Con este grafico podemos observar la distribución de precios de los vehículos usados en el mercado, 
                identificando que la mayoría de los vehículos se concentran en rangos de precio bajos a medios,
                y conforme el precio aumenta, la cantidad de vehículos disminuye, lo que es normal en este tipo de mercado.""")

    fig = px.histogram(
        df_filtered,
        x="price",
        nbins=100,
        labels={"price": "Precio (USD)", "count": "Número de vehículos"},
        title="Distribución de precios de vehículos usados"
    )
    st.plotly_chart(fig, use_container_width=True)


elif analysis_option == "Distribución del kilometraje":
    st.subheader("Distribución del kilometraje")

    st.markdown("""
     **Insight esperado:**  
                En Este grafico podemos observar la distribución del kilometraje de los vehículos usados en el mercado,
                donde se observa una alta concentracion de vehiculos con kilometrajes elevados,
                 esto coincide con el comportamiento del mercado de autos usados.
    """)

    fig = px.histogram(
        df_filtered,
        x="odometer",
        nbins=80,
        labels={"odometer": "Kilometraje (millas)", "count": "Número de vehículos"},
        title="Distribución del kilometraje"
    )
    st.plotly_chart(fig, use_container_width=True)


elif analysis_option == "Kilometraje vs Precio":
    st.subheader("Relación entre kilometraje y precio")

    st.markdown("""
     **Insight clave:**  
                En este grafico podemos observar la relación entre el kilometraje y el precio de los vehículos usados en el mercado.
                en donde se observa que existe una relación inversa entre ambas variables: a mayor kilometraje, menor precio.
                Sin embargo, el año del modelo introduce variabilidad en esta relación, 
                ya que vehículos más nuevos tienden a mantener precios más altos incluso con kilometrajes elevados.
    """)

    fig = px.scatter(
        df_filtered,
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
    **Insight clave:**  
    Camionetas y SUVs tienden a tener precios promedio más altos en comparación con sedanes y hatchbacks.
    """)

    avg_price_type = df_filtered.groupby("type", as_index=False)["price"].mean()

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
    **Insight clave:**  
    Los vehículos en mejor condición presentan precios significativamente más altos,
    y con una dispersión menor, esto coincide con los graficos anteriores donde se observa que los vehiculos con menor kilometraje (usualmente en mejor condición),
    tienden a tener precios más altos.
""")

    df_filtered["condition"] = pd.Categorical(
        df_filtered["condition"],
        categories=[
            "new", "like new", "excellent",
            "good", "fair", "salvage"
        ],
        ordered=True
    )

    fig = px.box(
        df_filtered,
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
    **Insight clave:**  
    Los vehículos eléctricos y diésel tienden a mostrar precios más altos
    en comparación con gasolina, esto puede reflejar la percepción de valor y costos asociados a estos tipos de combustible.
    mientras que los vehiculos electricos representan una menor cantidad en el mercado de usados, su precio es considerablemente más alto. 
    esto puede deberse a la demanda creciente y a la percepción de valor a largo plazo. 
    En el caso de los vehiculos diésel, suelen ser asociados con mayor durabilidad y eficiencia en consumo,
    mientras que los vehiculos a gasolina son los más comunes y presentan una mayor dispersión de precios.
    """)

    fig = px.box(
        df_filtered,
        x="fuel",
        y="price",
        color="fuel",
        labels={"fuel": "Tipo de combustible", "price": "Precio (USD)"},
        title="Precio por tipo de combustible"
    )
    st.plotly_chart(fig, use_container_width=True)

elif analysis_option == "Mapa de calor de correlaciones":
    st.subheader("Mapa de calor de correlaciones")

    st.markdown("""
    **Insight clave:**  
    Este mapa de calor muestra la relación entre variables numéricas del mercado
    de vehículos usados, permitiendo identificar correlaciones positivas y negativas
    relevantes para el análisis del precio.
    """)

    numeric_cols = [
        "price",
        "model_year",
        "odometer",
        "cylinders",
        "days_listed"
    ]

    corr_matrix = df_filtered[numeric_cols].corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        aspect="auto",
        title="Correlación entre variables numéricas"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
# ---------------------------
# Conclusiones del análisis
# ---------------------------
st.markdown("## Conclusiones del análisis")

avg_price = df_filtered["price"].mean()
avg_odometer = df_filtered["odometer"].mean()
avg_year = df_filtered["model_year"].mean()

most_common_type = df_filtered["type"].mode()[0]
most_common_fuel = df_filtered["fuel"].mode()[0]

st.markdown(f"""
### Hallazgos clave

- **Precio promedio:** ${avg_price:,.0f} USD  
- **Kilometraje promedio:** {avg_odometer:,.0f} millas  
- **Año promedio del modelo:** {int(avg_year)}  

### Características predominantes del mercado

- El tipo de vehículo más común en el segmento analizado es **{most_common_type}**.
- El tipo de combustible más frecuente es **{most_common_fuel}**, lo que refleja la composición dominante del mercado de vehículos usados.

---

### Relación precio–uso

- Se observa una relación inversamente proporcional entre el kilometraje y el precio:  
  vehículos con mayor kilometraje tienden a presentar precios más bajos.
- Sin embargo, el año del modelo atenúa este efecto, ya que modelos más recientes
  mantienen precios altos incluso con alto kilometraje.

---

### Implicaciones del análisis

- El mercado presenta una alta dispersión de precios, influenciada por múltiples factores
  como tipo de vehículo, condición y combustible.
- Este comportamiento sugiere que el precio no depende de una sola variable, sino de la
  combinación de características técnicas y de uso.
""")

st.markdown("---")
# ---------------------------
# Cierre
# ---------------------------
st.markdown("---")
st.markdown(
    " **Proyecto desarrollado con Python, Pandas, Plotly y Streamlit.**"
)
st.caption("Autor: Manuel Jacob Casariego Martínez")
    