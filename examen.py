# Importar librerías necesarias
import requests
import pandas as pd
import hashlib
import time
import sqlite3

# Función para obtener el nombre del idioma de un país desde restcountries.com y encriptarlo con SHA1
def obtener_nombre_idioma_y_encriptar(pais):
    url = f"https://restcountries.com/v3.1/name/{pais}"
    response = requests.get(url)
    try:
        data = response.json()
        idioma = data[0]['languages'][0]['name']

        # Encriptar el nombre del idioma con SHA1
        idioma_encriptado = hashlib.sha1(idioma.encode()).hexdigest()

        return idioma_encriptado
    except (KeyError, IndexError):
        return 'Datos del idioma no encontrados'

# Función para crear la tabla
def crear_tabla():
    # Crear un DataFrame vacío
    df = pd.DataFrame(columns=['País', 'Idioma_Encriptado', 'Tiempo'])

    paises = ['España', 'Francia', 'Italia']  # Ejemplo de países

    for pais in paises:
        tiempo_inicio = time.time()
        idioma_encriptado = obtener_nombre_idioma_y_encriptar(pais)
        tiempo_fin = time.time()
        tiempo_transcurrido = tiempo_fin - tiempo_inicio

        df.loc[len(df)] = [pais, idioma_encriptado, tiempo_transcurrido]

    # Calcular tiempo total, promedio, mínimo y máximo usando funciones de Pandas
    tiempo_total = df['Tiempo'].sum()
    tiempo_promedio = df['Tiempo'].mean()
    tiempo_minimo = df['Tiempo'].min()
    tiempo_maximo = df['Tiempo'].max()

    # Guardar el DataFrame en SQLite
    conn = sqlite3.connect('data.db')
    df.to_sql('paises', conn, if_exists='replace', index=False)

    # Generar JSON y guardarlo
    df.to_json('data.json', orient='records')

    return tiempo_total, tiempo_promedio, tiempo_minimo, tiempo_maximo

# Llamar a la función para crear la tabla
tiempo_total, tiempo_promedio, tiempo_minimo, tiempo_maximo = crear_tabla()

print(f"Tiempo Total: {tiempo_total}")
print(f"Tiempo Promedio: {tiempo_promedio}")
print(f"Tiempo Mínimo: {tiempo_minimo}")
print(f"Tiempo Máximo: {tiempo_maximo}")