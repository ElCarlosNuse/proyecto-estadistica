import streamlit as st
import pandas as pd

#Datos rapidos
poblacion= {'Pais': ['Venezuela', 'México', 'Colombia'],
            'Población': [28,126,50]}


st.scatter_chart(poblacion, x='Pais', y='Población')

#Unimos con streamlit (añdaimos el titulo)
st.title("Mapa Mundial de Población")
st.header("Mapa sobre la poblacion mundial")
st.write("Lentamente llegaremos al objetivo final ^^")


#Separamos en columnas 
columna_izq, columna_der = st.columns(2)

#Añadimos widgets
with columna_izq:
    nombre= st.sidebar.text_input("Por favor escriba su nombre")
    edad= st.slider("Ahora su edad")


with columna_der:
#Ahora un poco de logica 
    if nombre: #Si no se escribio nada
        st.sidebar.write(f"Hola {nombre}, tu edad es de {edad} años? apoco le atine")

continente = st.sidebar.selectbox(
    'En que continente te gustaría vivir?',
('Norte América', 'Europa', 'Asia'),
    index= None,
    placeholder="Debe seleccionar una opcion"
)

st.write(f"Bien usted a seleccionado el continente de {continente}, verdad?")

if st.checkbox('Mostrar informacion secreta'):
    st.write("Apoco te imaginabas haciendo esto a estas etapas jaja")


nivel = st.radio(
    "Elige tu nivel de sabiduria por favor:",
    ("Mago", "Experto", "Aprendis", "Aprendis mago"),
    index= None,)

if nivel == "Aprendis mago":
    st.write(f"USted tiene un nivel de experiencia muy grande señor sabio {nivel}")

    # 2. La Lógica Mágica (Datos de Latitud y Longitud)
if continente == 'Norte América':
    # Coordenadas aproximadas (Nueva York, Los Angeles, CDMX)
    datos_mapa = pd.DataFrame({
        'lat': [40.7128, 34.0522, 19.4326],
        'lon': [-74.0060, -118.2437, -99.1332]
    })
elif continente == 'Europa':
    # Coordenadas aproximadas (Londres, París, Berlín)
    datos_mapa = pd.DataFrame({
        'lat': [51.5074, 48.8566, 52.5200],
        'lon': [-0.1278, 2.3522, 13.4050]
    })
elif continente == 'Asia':
    # Coordenadas aproximadas (Tokio, Beijing, Delhi)
    datos_mapa = pd.DataFrame({
        'lat': [35.6762, 39.9042, 28.6139],
        'lon': [139.6503, 116.4074, 77.2090]
    })



#invocando el mapa
st.map(datos_mapa)