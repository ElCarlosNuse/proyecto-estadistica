#Importamos las librerias (pandas, plotly, streamlit)
import pandas as pd
import streamlit as st
import plotly.express as px

#Titulo y confiuración 
st.set_page_config(page_title="Proyecto (Individuos usando internet)", layout= "wide", page_icon="🌐" )
st.title("🌍 Acceso Global a Internet")
st.markdown("Datos del Banco Mundial analizados con Python")




# --- DICCIONARIO DE COORDENADAS (El GPS para que el mapa gire) ---
# Plotly no sabe dónde están los países, así que se lo decimos nosotros.
# He añadido los principales. Si falta alguno raro, el mapa simplemente no girará (se quedará quieto).
COORDENADAS_PAISES = {
    'Venezuela': {'lat': 6.4238, 'lon': -66.5897},
    'United States': {'lat': 37.0902, 'lon': -95.7129},
    'China': {'lat': 35.8617, 'lon': 104.1954},
    'Spain': {'lat': 40.4637, 'lon': -3.7492},
    'India': {'lat': 20.5937, 'lon': 78.9629},
    'Brazil': {'lat': -14.2350, 'lon': -51.9253},
    'Japan': {'lat': 36.2048, 'lon': 138.2529},
    'Germany': {'lat': 51.1657, 'lon': 10.4515},
    'France': {'lat': 46.2276, 'lon': 2.2137},
    'United Kingdom': {'lat': 55.3781, 'lon': -3.4360},
    'Russia': {'lat': 61.5240, 'lon': 105.3188},
    'Australia': {'lat': -25.2744, 'lon': 133.7751},
    'Mexico': {'lat': 23.6345, 'lon': -102.5528},
    'Argentina': {'lat': -38.4161, 'lon': -63.6167},
    'Colombia': {'lat': 4.5709, 'lon': -74.2973},
    'Canada': {'lat': 56.1304, 'lon': -106.3468},
    'Italy': {'lat': 41.8719, 'lon': 12.5674},
    'South Africa': {'lat': -30.5595, 'lon': 22.9375},
    'Nigeria': {'lat': 9.0820, 'lon': 8.6753},
    'Egypt': {'lat': 26.8206, 'lon': 30.8025},
    'Afghanistan': {'lat': 33.9391, 'lon':  67.7100}
}

# Usamos @st.cache_data para que no recargue el archivo cada vez que tocas un botón
@st.cache_data
def cargar_datos(): #Creamos la funcion para cargar los datos

    #Nombre del csv exacto que necesitamos
    archivo_csv = "API_IT.NET.USER.ZS_DS2_en_csv_v2_100.csv"

    #Leemos el CSV
    try:
        df = pd.read_csv(archivo_csv, skiprows=4)
        return df
    except FileNotFoundError:
        return None

#Ejecutamos la funcion 
df_bruto = cargar_datos()

if df_bruto is None:
    st.error("⚠️No se encuentra el archivo 🚧")
    st.stop()#Detiene la app para que no explote



#Ahora limpiamos el CSV ya que es muy robusto
def limpiar_datos(df): #Creamos la funcion
    datos= df[['Country Name', 'Country Code', '2023']]

    #Renombramos al español
    datos.columns= ['Pais', 'Codigo', 'Internet_Porc']

    # --- IMPORTANTE: LIMPIEZA DE NOMBRES ---
    # Esto arregla el problema de que el mapa no gire en Venezuela o Rusia
    reemplazos = {
        'Venezuela, RB': 'Venezuela',
        'Egypt, Arab Rep.': 'Egypt',
        'Korea, Rep.': 'South Korea',
        'Iran, Islamic Rep.': 'Iran',
        'Russian Federation': 'Russia',
        'Syrian Arab Republic': 'Syria',
        'Congo, Dem. Rep.': 'DR Congo',
        'United States': 'United States' # Aseguramos coincidencia
    }
    datos['Pais'] = datos['Pais'].replace(reemplazos)
    

    #Borramos los datos innecesarios (De paises que no reportaron)
    datos= datos.dropna()
    return datos

df_limpio = limpiar_datos(df_bruto)
#Verificacion rapida 
#st.write("Archivo Cargado. Primeras filas: ", df_limpio.head())

#Añadimos los datos mas recientes de Venezuela (Inexistentes a partir del año 2017 )

venezuela = pd.DataFrame({
    'Pais': ['Venezuela'],
    'Codigo': ['VEN'],
    'Internet_Porc': [61.6]
}) #Datos Aproximados para fines de 2025

#Concatenamos y pegamos a venezuela en la lista de paises
df_final = pd.concat([df_limpio, venezuela], ignore_index=True)#<-- Para que no se descontrolen los indicies

#Tabla final
#st.subheader("Datos para analizar")
#st.dataframe(df_final)

#--------------------------------------------
#Aqui empieza la interfaz
#---------------------------------------------


#Barra lateral (SIDEBAR)
st.sidebar.header("🔍 Panel de Control")
st.sidebar.write("Seleccione un pais para ver sus detalles específicos. ")

#Creamos una lista de paises ordenada
lista_paises= sorted(df_final['Pais'].unique())
pais_seleccionado= st.sidebar.selectbox("Selecciona un Pais: ", lista_paises)



#Rotación por pais (por defecto en coordenadas 0 0)
rotacion_lon= 0
rotacion_lat= 0

#Condicion para rotar los mapas (dependiendo del pais seleccionado)
if pais_seleccionado in COORDENADAS_PAISES:
    coords= COORDENADAS_PAISES[pais_seleccionado]
    rotacion_lat= coords['lat']
    rotacion_lon= coords['lon']

else:
    #Si el pais seleccionado no se encuentra dentro de los creados mostramos un mensaje de advertencia
    st.sidebar.warning(f"Auto-rotacion No activa para el pais // No se tienen las coordenadas del pais ({pais_seleccionado}) ")

#-------------------Mapa 3D---------------------------

st.success("✅ Datos cargados correctamente")
st.subheader("🗺️ Dashboard de Conectividad Global")


#En la barra lateral (SIDEBAR)
st.sidebar.markdown("---")
modo_turbo = st.sidebar.checkbox("🚀 Modo Rendimiento (optimizado)", value=True, help="Activa este boton si el mapa va lento")


#Definimos la proyeccion segun el modo 

if modo_turbo:
    proyeccion_activa= "equirectangular" #Modo plano mas òptimo
    st.sidebar.info("ℹ️ Modo 2D activado para mayor fluidez.")
    #solo permiimos movimientos de izquierda a derecha
    lat_final= 0
    lon_final= rotacion_lon

else: 
    proyeccion_activa= "orthographic" #Globo 3D (mejor pero mas pesado)
    st.sidebar.success("✨ Modo 3D activado.")
    lat_final = rotacion_lat
    lon_final = rotacion_lon


# 1. CREAMOS EL MAPA (Pero no lo mostramos todavía)
figura_mapa = px.choropleth(
    df_final, 
    locations="Codigo", 
    color="Internet_Porc",
    hover_name="Pais", 
    color_continuous_scale="Plasma",
    projection= proyeccion_activa,
    range_color= (0,100),
    title="", # Sin título para ahorrar espacio
)

# Ajustes estéticos del mapa
figura_mapa.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', # Fondo transparente para integrarse con el navegador
    plot_bgcolor='rgba(0,0,0,0)', # Fondo transparente del gráfico
    geo=dict(
        bgcolor='rgba(0,0,0,0)', # Hace transparente el fondo del mapa

        # --- TRUCO DE VELOCIDAD SUPREMA ---
        # 110 = Baja resolución (Líneas simples, Vuela en Canaima)
        # 50  = Alta resolución (Líneas detalladas, Lento)
        resolution=110,

        
        #Apartados de agua si esta en modo rendimiento elagua estara desactivada
        showocean= True,
        oceancolor="LightBlue",

        showcoastlines=False,

        showlakes= False,
        lakecolor="LightBlue",

        showrivers=False,
        rivercolor= "LightBlue",

        #Tierra

        showland=True,
        landcolor="white",


        showcountries=True,
        countrycolor="gray",

        showframe=False,

        # 5. LA ROTACIÓN AUTOMÁTICA
        projection_rotation=dict(
            lon=lon_final,  # Gira izquierda/derecha (OK en ambos)
            lat=lat_final,  # Gira arriba/abajo (SOLO en 3D, en 2D es 0)
            roll=0,
            ),
        ),


    margin={"r":0,"t":0,"l":0,"b":0},
    height=500 
    )# Altura fija para controlar el diseño




#Añadimos un resaltado adicional para el pais seleccionado 
if pais_seleccionado in COORDENADAS_PAISES:
    figura_mapa.add_scattergeo(
        lat= [COORDENADAS_PAISES[pais_seleccionado]['lat']],
        lon=[COORDENADAS_PAISES[pais_seleccionado]['lon']],
        mode='text',
        text="📶",
        textfont= dict(size= 20, color='gold'),
        name=pais_seleccionado
    )


# 2. PREPARAMOS LOS DATOS DEL PAÍS SELECCIONADO
datos_pais = df_final[df_final['Pais'] == pais_seleccionado]
porcentaje_pais = datos_pais['Internet_Porc'].values[0]
promedio_mundial = df_final['Internet_Porc'].mean()

# ------------------- DIVISIÓN EN COLUMNAS ---------------------------
# Creamos las dos columnas: Izquierda (Grande) y Derecha (Pequeña)
col_mapa, col_datos = st.columns([3, 1.3], gap="medium")

# --- COLUMNA IZQUIERDA: EL MAPA ---
with col_mapa:
    st.markdown("#### Vista Global")

    
    # Aquí mostramos el mapa directamente, SIN st.metric
    st.plotly_chart(figura_mapa, use_container_width=True)

# --- COLUMNA DERECHA: LOS DATOS ---
with col_datos:
    st.markdown(f"#### 📊 Análisis: {pais_seleccionado}")
    
    # A) El Veredicto
    if porcentaje_pais > 90:
        st.success("🚀 Excelente")
    elif porcentaje_pais > 50:
        st.warning("😐 Regular")
    else:
        st.error("😥 Baja")

    # B) Las Métricas
    st.metric(
        label="Acceso Internet",
        value=f"{porcentaje_pais:.1f}%",
        delta=f"{porcentaje_pais - promedio_mundial:.1f}% vs Mundo"
    )
    
    st.metric(label="Promedio Global", value=f"{promedio_mundial:.1f}%")

    st.write("---") 

    # C) El Gráfico de Barras (Pequeño)
    datos_grafico = pd.DataFrame({
        'Entidad': [pais_seleccionado, 'Mundo'],
        'Porcentaje': [porcentaje_pais, promedio_mundial]
    })

    figura_barras = px.bar(
        datos_grafico,
        x='Entidad', 
        y='Porcentaje',
        color='Entidad',
        text_auto='.1f',
        height=200 # Gráfico bajito para que quepa bien
    )
    
    # Limpiamos el gráfico para que se vea elegante en tamaño pequeño
    figura_barras.update_layout(
        showlegend=False, 
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_title=None,
        yaxis_title=None,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # Texto blanco para que se lea en modo oscuro
        font=dict(color="white")
    )
    
    st.plotly_chart(figura_barras, use_container_width=True)