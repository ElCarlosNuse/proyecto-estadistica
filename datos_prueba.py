import pandas as pd 

def cargar_datos_prueba():
#Genera datos estadisticos los cuales se usaran para probar la interfaz (prototipo)
    datos_2026 = { 
        'codigo_abre' : ['VEN', 'BRA', 'ARG', 'CHL', 'COL', 'ESP', 'USA', 'JPN', 'FRA', 'AUS'],
        'pais' : ['Venezuela', 'Brasil', 'Argentina', 'Chile', 'Colombia', 'España', 'Estados Unidos', 'Japón', 'Francia', 'Australia'],
        'meta_año' : ['IA Avanzada', 'Energía Verde', 'Red 6G', 'Computación Cuántica', 'Ciudades Inteligentes', 'Turismo Tech', 'Chips', 'Robótica', 'Startups', 'Ciberseguridad'],
        'progreso' : [70, 75, 55, 60, 65, 80, 95, 88, 82, 78],
        # Coordenadas aproximadas para cada país
        'latitud' : [8, -14, -34, -33, 4, 40, 39, 36, 46, -25],
        'longitud' : [-66, -53, -64, -70, -73, -3, -98, 139, 2, 133] }
    return pd.DataFrame(datos_2026)