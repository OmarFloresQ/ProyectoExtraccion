import mysql.connector
import pandas as pd

file_path = 'jugadoresdatos.csv'
df = pd.read_csv(file_path)

df[['Equipo', 'Posición']] = df['Equipo'].str.split(' - ', expand=True)

conexion = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Hmclcma03.'
)

cursor = conexion.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS futbol")

cursor.execute("USE futbol")

cursor.execute("""
CREATE TABLE IF NOT EXISTS jugadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    equipo VARCHAR(255),
    posicion VARCHAR(255),
    minutos_jugados INT,
    partidos INT,
    goles INT,
    asistencias INT,
    distancia_cubierta FLOAT,
    top_speed FLOAT
)""")

for index, row in df.iterrows():
    cursor.execute("""
    INSERT INTO jugadores (nombre, equipo, posicion, minutos_jugados, partidos, goles, asistencias, distancia_cubierta, top_speed)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['Nombre'], row['Equipo'], row['Posición'], row['Minutos Jugados'], row['Partidos'], row['Goles'], row['Asistencias'], row['Distancia Cubierta'], row['Top Speed']))

cursor.execute("""
CREATE TABLE IF NOT EXISTS equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS posiciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS estadisticas_posiciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    posicion_id INT,
    promedio_goles FLOAT,
    promedio_asistencias FLOAT,
    promedio_distancia_cubierta FLOAT,
    promedio_top_speed FLOAT,
    FOREIGN KEY (posicion_id) REFERENCES posiciones(id)
)""")

equipos = df['Equipo'].unique()
for equipo in equipos:
    cursor.execute("INSERT IGNORE INTO equipos (nombre) VALUES (%s)", (equipo,))

posiciones = df['Posición'].unique()
for posicion in posiciones:
    cursor.execute("INSERT IGNORE INTO posiciones (nombre) VALUES (%s)", (posicion,))

goles_por_posicion = df.groupby('Posición')['Goles'].mean()
asistencias_por_posicion = df.groupby('Posición')['Asistencias'].mean()
distancia_por_posicion = df.groupby('Posición')['Distancia Cubierta'].mean()
velocidad_por_posicion = df.groupby('Posición')['Top Speed'].mean()

estadisticas = pd.DataFrame({
    'Promedio Goles': goles_por_posicion,
    'Promedio Asistencias': asistencias_por_posicion,
    'Promedio Distancia Cubierta': distancia_por_posicion,
    'Promedio Top Speed': velocidad_por_posicion
})

for index, row in estadisticas.iterrows():
    cursor.execute("""
    INSERT INTO estadisticas_posiciones (posicion_id, promedio_goles, promedio_asistencias, promedio_distancia_cubierta, promedio_top_speed)
    VALUES ((SELECT id FROM posiciones WHERE nombre = %s), %s, %s, %s, %s)
    """, (index, row['Promedio Goles'], row['Promedio Asistencias'], row['Promedio Distancia Cubierta'], row['Promedio Top Speed']))

conexion.commit()
cursor.close()
conexion.close()
