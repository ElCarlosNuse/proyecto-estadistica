#Importamos las librerias (pandas, plotly, streamlit)
import pandas as pd
import streamlit as st
import plotly.express as px
import zipfile #<-- Para leer los archivos zip sin descomprimirlos

#Titulo y confiuración 
st.set_page_config(page_title="Proecto (Individuos usando internet)", layout= "wide")
st.title("🌍 Acceso Global a Internet")
st.markdown("Datos del Banco Mundial analizados con Python")


#Carga de los datos desde el ZIP
# Usamos @st.cache_data para que no recargue el archivo cada vez que tocas un botón
@st.cache_data
def cargar_datos(): #Creamos la funcion para cargar los datos
    #Nombre del archivo
    archivo_zip = "datos_base.zip"

    #Nombre del csv exacto que necesitamos
    archivo_csv = "API_IT.NET.USER.ZS_DS2_en_csv_v2_100.csv"

    #Abrimos el zip
    with zipfile.ZipFile(archivo_zip, "r") as z:
        #Abrimos el csv especifico y saltamos las primeras 4 lineas
        with z.open(archivo_zip) as f:
            df = pd.read_csv(f, skiprows=4)
    return df

#Ejecutamos la funcion
df_bruto = cargar_datos()

#Verificacion rapida 
st.write("Archivo Cargado. Primeras filas: ", df_bruto.head())