import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash, dash_table, Input, Output
from sqlalchemy import create_engine


conexion = 'mysql+mysqlconnector://root:Hmclcma03.@127.0.0.1/futbol'
crearconexion = create_engine(conexion)

df_jugadores = pd.read_sql('SELECT * FROM jugadores', crearconexion)
df_equipos = pd.read_sql('SELECT * FROM equipos', crearconexion)
df_posiciones = pd.read_sql('SELECT * FROM posiciones', crearconexion)
df_estadisticas_posiciones = pd.read_sql('SELECT * FROM estadisticas_posiciones', crearconexion)
#De esta manera extraigo los datos de mi base de datos para de esa manera poder mandarlos a mis dashboards mas facilmente

def limpieza2(df, subset=None):
    df = df.drop_duplicates(subset=subset)  # Elimino duplicados basados en la columna nombre ya que es la mas facil de identificar
    df = df.dropna()  # Elimino nulos
    return df

df_jugadores = limpieza2(df_jugadores, subset='nombre')
df_equipos = limpieza2(df_equipos, subset='nombre')
df_posiciones = limpieza2(df_posiciones, subset='nombre')
df_estadisticas_posiciones = limpieza2(df_estadisticas_posiciones)

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

def tarjetas_filtro():
    return dbc.Card(
        dbc.CardBody([
            html.H5("Filtro de Datos", className="card-title", style={"color": "white", "textAlign": "center"}),
            html.Div([
                dbc.Label("Posición", style={"color": "white"}),
                dcc.Dropdown(
                    options=[{"label": pos, "value": pos} for pos in df_posiciones['nombre'].unique()],
                    id="ddlPosicion",
                    multi=True,
                    value=[]
                )
            ]),
            html.Div([
                dbc.Label("Equipo", style={"color": "white"}),
                dcc.Dropdown(
                    options=[{"label": eq, "value": eq} for eq in df_equipos['nombre'].unique()],
                    id="ddlEquipo",
                    multi=True,
                    value=[]
                )
            ])
        ])
    )

@app.callback(
    Output("Figurajugadores1", "figure"),
    Output("TablaJugadores1", "data"),
    Output("Figurajugadores2", "figure"),
    Output("TablaJugadores2", "data"),
    Output("Figurajugadores3", "figure"),
    Output("TablaJugadores3", "data"),
    Input("ddlPosicion", "value"),
    Input("ddlEquipo", "value"),
)
def actualizargraf(value_posicion, value_equipo):
    df_filtrado = df_jugadores.copy()

    if value_posicion:
        df_filtrado = df_filtrado[df_filtrado['posicion'].isin(value_posicion)]

    if value_equipo:
        df_filtrado = df_filtrado[df_filtrado['equipo'].isin(value_equipo)]

    figura1 = px.bar(df_filtrado, x="nombre", y="goles", title="¿Cuántos goles ha anotado cada jugador?", color="goles", color_continuous_scale=px.colors.sequential.Greys)
    figura1.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white", title={"text": "¿Cuántos goles ha anotado cada jugador?", "x": 0.5, "xanchor": "center"})

    figura2 = px.bar(df_filtrado, x="nombre", y="asistencias", title="¿Cuántas asistencias ha realizado cada jugador?", color="asistencias", color_continuous_scale=px.colors.sequential.Greys)
    figura2.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white", title={"text": "¿Cuántas asistencias ha realizado cada jugador?", "x": 0.5, "xanchor": "center"})

    figura3 = px.scatter(df_filtrado, x="minutos_jugados", y="distancia_cubierta", title="¿Cómo se relacionan los minutos jugados y la distancia cubierta por cada jugador?", color="minutos_jugados", color_continuous_scale=px.colors.sequential.Greys, size="distancia_cubierta", text="nombre")
    figura3.update_traces(textposition='top center')
    figura3.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white", title={"text": "¿Cómo se relacionan los minutos jugados y la distancia cubierta por cada jugador?", "x": 0.5, "xanchor": "center"})

    tabla1 = df_filtrado[['nombre', 'equipo', 'posicion', 'goles']].to_dict('records')
    tabla2 = df_filtrado[['nombre', 'equipo', 'posicion', 'asistencias']].to_dict('records')
    tabla3 = df_filtrado[['nombre', 'equipo', 'posicion', 'minutos_jugados', 'distancia_cubierta']].to_dict('records')

    return figura1, tabla1, figura2, tabla2, figura3, tabla3

def dash_layout1():
    return html.Div([
        html.H1("Estadísticas Generales de Jugadores", style={"textAlign": "center", "color": "white"}),
        html.P("Estadísticas Generales de Jugadores de la Champions League Omar Flores Becerril", style={"color": "white", "textAlign": "center"}),
        html.Hr(style={"borderColor": "white"}),
        tarjetas_filtro(),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(dash_table.DataTable(
                        id="TablaJugadores1",
                        page_size=10,
                        style_header={'backgroundColor': 'rgb(30,30,30)', 'color': 'white'},
                        style_cell={'textAlign': 'left', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                        style_table={'height': '400px', 'overflowY': 'auto'}
                    ), width=5, style={'display': 'flex', 'alignItems': 'center'}),
                    dbc.Col(dcc.Graph(id="Figurajugadores1", style={'height': '65vh'}), width=7)
                ]),
                dbc.Row([
                    dbc.Col(dash_table.DataTable(
                        id="TablaJugadores2",
                        page_size=10,
                        style_header={'backgroundColor': 'rgb(30,30,30)', 'color': 'white'},
                        style_cell={'textAlign': 'left', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                        style_table={'height': '400px', 'overflowY': 'auto'}
                    ), width=5, style={'display': 'flex', 'alignItems': 'center'}),
                    dbc.Col(dcc.Graph(id="Figurajugadores2", style={'height': '65vh'}), width=7)
                ]),
                dbc.Row([
                    dbc.Col(dash_table.DataTable(
                        id="TablaJugadores3",
                        page_size=10,
                        style_header={'backgroundColor': 'rgb(30,30,30)', 'color': 'white'},
                        style_cell={'textAlign': 'left', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                        style_table={'height': '400px', 'overflowY': 'auto'}
                    ), width=5, style={'display': 'flex', 'alignItems': 'center'}),
                    dbc.Col(dcc.Graph(id="Figurajugadores3", style={'height': '65vh'}), width=7)
                ])
            ], width=12)
        ])
    ], style={"backgroundColor": "black"})

@app.callback(
    Output("Figuragoles", "figure"),
    Output("TablaGoles", "data"),
    Output("FiguraAsistencias", "figure"),
    Output("TablaAsistencias", "data"),
    Output("Figuradistancias", "figure"),
    Output("TablaDistancias", "data"),
    Input("ddlPosicion", "value"),
    Input("ddlEquipo", "value"),
)
def actualizargarf2(value_posicion, value_equipo):
    df_filtrado = df_jugadores.copy()

    if value_posicion:
        df_filtrado = df_filtrado[df_filtrado['posicion'].isin(value_posicion)]

    if value_equipo:
        df_filtrado = df_filtrado[df_filtrado['equipo'].isin(value_equipo)]

    figuragoles = px.pie(df_filtrado, values='goles', names='posicion', title="¿Cómo se distribuyen los goles por posición?", color_discrete_sequence=px.colors.sequential.Greys)
    figuragoles.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white", title={"text": "¿Cómo se distribuyen los goles por posición?", "x": 0.5, "xanchor": "center"})

    figuraasistencias = px.box(df_filtrado, x="posicion", y="asistencias", title="¿Cómo se distribuyen las asistencias por posición?", color_discrete_sequence=px.colors.sequential.Greys)
    figuraasistencias.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white", title={"text": "¿Cómo se distribuyen las asistencias por posición?", "x": 0.5, "xanchor": "center"})

    figuradistancia = px.bar(df_filtrado, x="posicion", y="distancia_cubierta", text='nombre', title="¿Cuál es el promedio de distancia cubierta por posición?", color='distancia_cubierta')
    figuradistancia.update_traces(textposition='outside')
    figuradistancia.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white", uniformtext_minsize=8, uniformtext_mode='hide', title={"text": "¿Cuál es el promedio de distancia cubierta por posición?", "x": 0.5, "xanchor": "center"})

    tabla_goles = df_filtrado[['nombre', 'equipo', 'posicion', 'goles']].to_dict('records')
    tabla_asistencias = df_filtrado[['nombre', 'equipo', 'posicion', 'asistencias']].to_dict('records')
    tabla_distancias = df_filtrado[['nombre', 'equipo', 'posicion', 'distancia_cubierta']].to_dict('records')

    return figuragoles, tabla_goles, figuraasistencias, tabla_asistencias, figuradistancia, tabla_distancias

def dash_layout2():
    return html.Div([
        html.H1("Estadísticas por Posición", style={"textAlign": "center", "color": "white"}),
        html.P("Hola una cordial bienvenida a los dashboards estadísticos de mi proyecto de programación para la extracción de datos.", style={"color": "white", "textAlign": "center"}),
        html.Hr(style={"borderColor": "white"}),
        tarjetas_filtro(),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(dash_table.DataTable(
                        id="TablaGoles",
                        page_size=10,
                        style_header={'backgroundColor': 'rgb(30,30,30)', 'color': 'white'},
                        style_cell={'textAlign': 'left', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                        style_table={'height': '400px', 'overflowY': 'auto'}
                    ), width=5, style={'display': 'flex', 'alignItems': 'center'}),
                    dbc.Col(dcc.Graph(id="Figuragoles", style={'height': '65vh'}), width=7)
                ]),
                dbc.Row([
                    dbc.Col(dash_table.DataTable(
                        id="TablaAsistencias",
                        page_size=10,
                        style_header={'backgroundColor': 'rgb(30,30,30)', 'color': 'white'},
                        style_cell={'textAlign': 'left', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                        style_table={'height': '400px', 'overflowY': 'auto'}
                    ), width=5, style={'display': 'flex', 'alignItems': 'center'}),
                    dbc.Col(dcc.Graph(id="FiguraAsistencias", style={'height': '65vh'}), width=7)
                ]),
                dbc.Row([
                    dbc.Col(dash_table.DataTable(
                        id="TablaDistancias",
                        page_size=10,
                        style_header={'backgroundColor': 'rgb(30,30,30)', 'color': 'white'},
                        style_cell={'textAlign': 'left', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                        style_table={'height': '400px', 'overflowY': 'auto'}
                    ), width=5, style={'display': 'flex', 'alignItems': 'center'}),
                    dbc.Col(dcc.Graph(id="Figuradistancias", style={'height': '65vh'}), width=7)
                ])
            ], width=12)
        ])
    ], style={"backgroundColor": "black"})

app.layout = html.Div([
    dbc.Tabs([
        dbc.Tab(label="Dashboard General", tab_id="pestaña1"),
        dbc.Tab(label="Dashboard por Posición", tab_id="pestaña2"),
    ],
        id="pestañas",
        active_tab="pestaña1",
    ),
    html.Div(id="pestaña_cobtenido")
], style={"backgroundColor": "black"})

# Callback para actualizar el contenido de las pestañas
@app.callback(
    Output("pestaña_cobtenido", "children"),
    Input("pestañas", "active_tab")
)
def switch_tab(at):
    if at == "pestaña1":
        return dash_layout1()
    elif at == "pestaña2":
        return dash_layout2()
    return html.P("This shouldn't ever be displayed...")

if __name__ == "__main__":
    app.run(debug=True)
