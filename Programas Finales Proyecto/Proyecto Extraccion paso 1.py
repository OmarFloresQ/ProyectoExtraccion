import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options

opciones = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opciones)
driver.get('https://www.uefa.com/uefachampionsleague/statistics/players/')
time.sleep(3)

datos = []
jugadores_recolectados = set()
numero_scrolls = 20 #Por favor poner aqui los ciclos que desea checar profe
tiempo_entre_scroll = 2
tamaño_scroll = 1205 #Con este tamaño de sroll a mi me funciono si necesita modificarlo lo puede hacer nada mas calcular de 50 en 50 y de esa manera sera mucho mas facil
incremento_scroll = 50

scrolls_realizados = 0
while scrolls_realizados < numero_scrolls:
    ventana = driver.execute_script("return document.body.scrollHeight")
    nuevaventana = 0
    posicion_actual = 0
    while nuevaventana < ventana and scrolls_realizados < numero_scrolls:
        driver.execute_script(f"window.scrollTo(0, {posicion_actual + tamaño_scroll});")
        time.sleep(tiempo_entre_scroll)
        nueva_altura = driver.execute_script("return document.body.scrollHeight")
        if nueva_altura == ventana:
            driver.execute_script(f"window.scrollTo(0, {posicion_actual + incremento_scroll});")
            time.sleep(tiempo_entre_scroll)
            posicion_actual += incremento_scroll
        else:
            posicion_actual += tamaño_scroll
        if nueva_altura > ventana:
            ventana = nueva_altura
        scrolls_realizados += 1

pagina = driver.page_source
htmlde_pagina = BeautifulSoup(pagina, 'html.parser')

contenido = htmlde_pagina.find('div', class_='content')
if contenido:
    contenido_ = contenido.find('div', class_='pk-container')
    if contenido_:
        jugadores = contenido_.find_all('div', class_='ag-row')
        for jugador in jugadores:
            nombre = jugador.find('span', {'slot': 'primary'}).text.strip()
            if nombre not in jugadores_recolectados:
                equipo = jugador.find('span', {'slot': 'secondary'}).text.strip()
                minutos_jugados = jugador.find('div', {'col-id': 'minutes_played_official'}).text.strip()
                partidos = jugador.find('div', {'col-id': 'matches_appearance'}).text.strip()
                goles = jugador.find('div', {'col-id': 'goals'}).text.strip()
                asistencias = jugador.find('div', {'col-id': 'assists'}).text.strip()
                distancia_cubierta = jugador.find('div', {'col-id': 'distance_covered'}).text.strip()
                top_speed = jugador.find('div', {'col-id': 'top_speed'}).text.strip()

                datos.append([nombre, equipo, minutos_jugados, partidos, goles, asistencias, distancia_cubierta, top_speed])
                jugadores_recolectados.add(nombre)

                if len(datos) >= 300:
                    break

driver.quit()

df = pd.DataFrame(datos, columns=['Nombre', 'Equipo', 'Minutos Jugados', 'Partidos', 'Goles', 'Asistencias',
                                  'Distancia Cubierta', 'Top Speed'])

df.to_csv('jugadoresdatos.csv', index=False)
print(f"Se han extraído datos de {len(df)} jugadores.")
