import streamlit as st
import plotly.express as px
from datos_prueba import cargar_datos_prueba #Importamos la funcion para cargar los datos de prueba 

#Configuracion de la pagina 

st.set_page_config(page_title="Prototipo V1", layout="wide")

#Titulo de la pagina 
st.title("Version 1: Prototipo Metas Tecnologicas 2026")
st.info("Este prototipo muestra un mapa interactivo con los datos locales (Diccionarios) de los paises y sus metas ")

#2 Cargando los datos de prueba 

try: 
    df = cargar_datos_prueba()

except Exception as e:
    st.error(f"Error al cargar los datos de prueba: {e}")
    st.stop()

#Interfaz 
col1, col2 = st.columns([1, 4])

with col1:
    st.subheader("Control")
    paises = ["Ver Todo"] + list(df['pais'])
    seleccion = st.selectbox("Filtrar por País", paises)

    #Logica de Coordenadas 

    if seleccion != "Ver Todo":
        dato = df[df["pais"] == seleccion].iloc[0]
        rotacion = dict(lon=dato['longitud'], lat=dato['latitud'], roll=0)
        zoom= 1.6
    else: 
        rotacion= dict(lon=-66, lat=10, roll=0)
        zoom= 1.0


    #Grafio

    fig = px.choropleth(
        df,
        locations="codigo_abre",
        color="progreso",
        hover_name="pais",
        hover_data={'codigo_abre': False, 'progreso': True, 'meta_año': True},
        color_continuous_scale= 'Viridis',
        projection="orthographic",
    ) 

    fig.update_layout(
        height=600,
        margin={"r":0,"t":0,"l":0,"b":0},
        geo= dict(
            showframe=False,
            showcoastlines=True,
            projection_rotation=rotacion,
            projection_scale=zoom,
            showocean=True,
            oceancolor="LightBlue"
        )
    )

    with col2: 
        st.plotly_chart(fig, use_container_width=True)