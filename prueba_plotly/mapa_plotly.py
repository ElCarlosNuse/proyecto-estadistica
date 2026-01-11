import plotly.express as px
import pandas as pd

#Creamos la libreria 

datos= { 
    'pais': ['Venezuela', 'Japon', 'España'],
    'ISO' : [ 'VEN', 'JPN', 'ESP'],
    'poblacio_millo' : [28, 140, 48]
}


#Convertimos el dicc en data frame 
df = pd.DataFrame(datos)
print(df)


#Creamos el mapa con plotly
figura= px.choropleth(
    df,
    locations= 'ISO',
    projection= 'orthographic',
    color= 'poblacio_millo',
    hover_name= 'pais'
)
figura.update_layout( 
    geo =dict(
    showcoastlines= True,
    showland= True,
    landcolor= "grey"

    )
)

figura.show()
