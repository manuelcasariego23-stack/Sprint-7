# Analisis de vehículos Usados en EE.UU.
Dashboard interactivo desarrollado con Phyton y Streamlit para realizar un análisis exploratorio de datos (EDA) sobre el mercado devehiculos usados en Estados Unidos, El Objetivo del proyecto es identificar patrones de precios, kilometraje y caracteristicas tecnicas, asi como comunicar insigths de forma clara mediante visualizaciones interactivas. 

# Objetivos 
Explorar y analizar un conjunto de datos de vehiculos usados para: 
    * Comprender la distribucion de precios de acuerdo al kilometraje
    * Analizar la relacion entre precio, uso y antigüedad
    *Evaluar cómo las variables: tipo de vehiculo, combustible y condicion influyen en el precio. 
    *Presentar los resultados graficamente en un dashboard interactivo. 

# Dataset
Fuente: dataset público de anuncios de vehículos usados en EE.UU.
Observaciones: Anuncios individuales de vehículos
Variables clave: 
price: Precio del vehículo (USD)

odometer: Kilometraje (millas)

model_year: Año del modelo

type: Tipo de vehículo

fuel: Tipo de combustible

condition: Condición del vehículo

days_listed: Días en publicación

# Limpieza y preparación de datos 
Para el procesamiento del dataset se realizaron las siguientes acciones: 

Correccion de Valores fatantes: 
    Model_year y odometer: mediana
    Cylinders: moda
    paint_color: categoría "unknown"
    is_4wd: valor 0 
Validación de tipos de datos y consistencia. 
Creacion de un dataset limpio para análisis y visualización. 

# Análisis y visualizaciones 

El Dashboard incluye los siguientes analisis interactivos:

    * Distribución de precios: Identificacion de concentracion en rangos bajos y medios 
    * Distribucion del kilometraje: Alta precencia de vehiculos con uso elevado 
    * Kilometraje VS precio: Relacion inversamente proporcional entre uso y valor, moderada por la antigüedad del vehiculo
    * Precio promedio por tipo de vehiculo: SUVs y camionetas precentan precios más altos 
    * Precio según condicion: vehiculos en mejor estado tienen un precio mas elevado
    * Precio por tipo de combustible: Vehículos eléctricos y diésel muestran precios promedio superiores
    * Mapa de calor de correlaciones: Relacion entre las distintas variables clave

Cada visualizacion tiene insigths clave que refuerzan el análisis del negocio. 

# Indicadores clave 

    * Precio promedio del mercado 
    * Kilometraje promedio
    * Año promedio del modelo 
    * Tipo de vehículo y combustible más comunes 

Estos KPIs permiten una vesion rápida del estado del mercado bajo distintos filtros. 


# Recursos utilizados 

- Python 3.10
- Pandas - Manipulación y limpieza de datos 
- Plotly-express - Visualizaciones interactivas 
- Streamlit - Desarrollo del dashboard
- git & GitHub - Control de Versiones 

# Ejecucion local 
bash 
git clone [text](https://github.com/manuelcasariego23-stack/Sprint-7)
cd Sprint-7
pip install -r requirements.txt
streamlit run app.py

# Resultados y conclusiones 
    * El precio de los vehículos usados depende de múltiples factores, no de una sola variable.

    * Existe una clara relación inversa entre kilometraje y precio, moderada por el año del modelo.

    * El mercado muestra alta dispersión de precios, especialmente en gasolina y sedanes.

    * SUVs, camionetas y vehículos eléctricos tienden a mantener precios más altos.

#Autor 
Manuel Jacob Casariego Martínez 
Msc.| Data Analyst | Python | EDA | Visualización de datos