import pandas as pd

file_path = 'jugadoresdatos.csv'
df = pd.read_csv(file_path)

Valores_faltantes = df.isnull().sum()
ducplicados = df.duplicated().sum()
Estadisticas = df.describe()


print("Valores faltantes por columna:")
print(Valores_faltantes , "\n")
print("Número de filas duplicadas:")
print(ducplicados, "\n")
print("Estadísticas descriptivas:")
print(Estadisticas)

df[['Equipo', 'Posición']] = df['Equipo'].str.split(' - ', expand=True)


df['Distancia Cubierta'] = pd.to_numeric(df['Distancia Cubierta'], errors='coerce')
df['Top Speed'] = pd.to_numeric(df['Top Speed'], errors='coerce')

stats_after = df.describe()

df.head()
goles_por_posicion = df.groupby('Posición')['Goles'].mean()
asistencias_por_posicion = df.groupby('Posición')['Asistencias'].mean()
distancia_por_posicion = df.groupby('Posición')['Distancia Cubierta'].mean()
velocidad_por_posicion = df.groupby('Posición')['Top Speed'].mean()

print("Promedio de Goles por Posición:")
print(goles_por_posicion,"\n")
print("Promedio de Asistencias por Posición:")
print(asistencias_por_posicion, "\n")
print("Promedio de Distancia Cubierta por Posición:")
print(distancia_por_posicion, "\n")
print("Promedio de Velocidad Máxima por Posición:")
print(velocidad_por_posicion, "\n")
