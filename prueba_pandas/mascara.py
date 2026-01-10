import pandas as pd 

#Creamos el diccionario manual 

datos= { 
    'pais': ['Venezuela', 'Colombia', 'Argentina', 'Japón', 'México', 'El Salvador', 'Chile'],
    'continente': ['América', 'América', 'América', 'Asia', 'América', 'América', 'América'],
    'poblacion_millones': [28, 50, 45, 126, 128, 6.5, 19],}

#Pasamos la lbreria a un dataFrame(df)

df = pd.DataFrame(datos)

print("-------------1. Esta es la tabla completa (DATARAME)-------------")
print(df)
print("\n")


#Ahora vamos filtrar la tabla por un pais
mascara= df['pais'] == 'Japón'  #Creamos la mascara para filtrar el pais

print("-------------2. esta es la mascara de True/False-------------")
print("Pyhn estara revisando fila por fila: ¿Eres Japón? Si es así, marca True, si no, marca False")
print(mascara)
print("Esta mascara nos ayudara a filtrar el DataFrame (solo dira True Donde este Japón)")
print("\n")

#Filtro ahora si aplicamos la mascara

resultado= df[mascara] #Aplicamos la mascara al DataFrame

print("-------------3. Este es el resultado final con la tabla ya filtrada-------------")
print(resultado)
print("\n")

#Ahora podemos extraer el dato con (.iloc[0])
print("El dato individual (.iloc[0]) de la poblacion de Japón es:")
try:
    #Tommamos la primera fila del resultado
    dato_limpio = resultado.iloc[0]
    print("Ya no es una tabla es un objeto con datos: ")
    print(f"Población : {dato_limpio['poblacion_millones']} millones")
    
except Exception as e: 
    print("No se encontró NADA"[e]) #Guardamos el error en la variable 'e'