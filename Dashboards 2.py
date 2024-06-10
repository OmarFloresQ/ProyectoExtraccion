import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash, dash_table, Input, Output

df = pd.read_csv("jugadoresdatos.csv")
df[['Equipo', 'Posición']] = df['Equipo'].str.split(' - ', expand=True)

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

def tarjetas_filtro():
    return dbc.Card(
        dbc.CardBody([
            html.H5("Filtro de Datos", className="card-title", style={"color": "white"}),
            html.Div([
                dbc.Label("Posición", style={"color": "white"}),
                dcc.Dropdown(
                    options=[{"label": pos, "value": pos} for pos in ["ALL"] + df['Posición'].unique().tolist()],
                    id="ddlPosicion",
                    value="ALL"
                )
            ]),
            html.Div([
                dbc.Label("Equipo", style={"color": "white"}),
                dcc.Dropdown(
                    options=[{"label": eq, "value": eq} for eq in ["ALL"] + df['Equipo'].unique().tolist()],
                    id="ddlEquipo",
                    value="ALL"
                )
            ])
        ])
    )

@app.callback(
    Output("Figurajugadores1", "figure"),
    Output("Figurajugadores2", "figure"),
    Output("Figurajugadores3", "figure"),
    Output("Tabla", "data"),
    Input("ddlPosicion", "value"),
    Input("ddlEquipo", "value"),
)
def actualizargraf(value_posicion, value_equipo):
    df_filtrado = df.copy()

    if value_posicion != "ALL":
        df_filtrado = df_filtrado[df_filtrado['Posición'] == value_posicion]

    if value_equipo != "ALL":
        df_filtrado = df_filtrado[df_filtrado['Equipo'] == value_equipo]

    figura1 = px.bar(df_filtrado, x="Nombre", y="Goles", title="Goles por Jugador", color="Goles", color_continuous_scale=px.colors.sequential.Greys)
    figura1.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white")

    figura2 = px.bar(df_filtrado, x="Nombre", y="Asistencias", title="Asistencias por Jugador", color="Asistencias", color_continuous_scale=px.colors.sequential.Greys)
    figura2.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white")

    figura3 = px.scatter(df_filtrado, x="Minutos Jugados", y="Distancia Cubierta", title="Minutos Jugados vs. Distancia Cubierta", color="Minutos Jugados", color_continuous_scale=px.colors.sequential.Greys, size="Distancia Cubierta")
    figura3.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white")

    return figura1, figura2, figura3, df_filtrado.to_dict("records")

def dash_layout1(data: pd.DataFrame):
    return html.Div([
        html.H1("Estadísticas Generales de Jugadores", style={"textAlign": "center", "color": "white"}),
        html.P("Estadisticas Generales de Jugadores de la champions league Omar Flores Becerril", style={"color": "white"}),
        html.Hr(style={"borderColor": "white"}),
        dbc.Row([
            dbc.Col(tarjetas_filtro(), width=4),
            dbc.Col([
                dash_table.DataTable(
                    id="Tabla",
                    data=data.to_dict("records"),
                    page_size=10,
                    style_header={'backgroundColor': 'rgb(30,30,30)', 'color': 'white'},
                    style_cell={'textAlign': 'left', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'}
                ),
                dcc.Graph(id="Figurajugadores1"),
                dcc.Graph(id="Figurajugadores2"),
                dcc.Graph(id="Figurajugadores3")
            ], width=8),
        ])
    ], style={"backgroundColor": "black"})

# Estadísticas para los dashboards
golexposicion = df.groupby('Posición')['Goles'].mean().reset_index()
asistenciasxposicion = df.groupby('Posición')['Asistencias'].mean().reset_index()
distanciaxposicion = df.groupby('Posición')['Distancia Cubierta'].mean().reset_index()

@app.callback(
    Output("Figuragoles", "figure"),
    Output("FiguraAsistencias", "figure"),
    Output("Figuradistancias", "figure"),
    Input("ddlPosicion", "value"),
    Input("ddlEquipo", "value"),
)
def actualizargarf2(value_posicion, value_equipo):
    df_filtrado = df.copy()

    if value_posicion != "ALL":
        df_filtrado = df_filtrado[df_filtrado['Posición'] == value_posicion]

    if value_equipo != "ALL":
        df_filtrado = df_filtrado[df_filtrado['Equipo'] == value_equipo]

    figuragoles = px.pie(df_filtrado, values='Goles', names='Posición', title="Distribución de Goles por Posición", color_discrete_sequence=px.colors.sequential.Greys)
    figuragoles.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white")

    figuraasistencias = px.box(df_filtrado, x="Posición", y="Asistencias", title="Distribución de Asistencias por Posición", color_discrete_sequence=px.colors.sequential.Greys)
    figuraasistencias.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white")

    figuradistancia = px.line(df_filtrado, x="Posición", y="Distancia Cubierta", title="Promedio de Distancia Cubierta por Posición", markers=True, color_discrete_sequence=px.colors.sequential.Greys)
    figuradistancia.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white")

    return figuragoles, figuraasistencias, figuradistancia

def dash_layout2():
    figuragoles = px.pie(golexposicion, values='Goles', names='Posición', title="Distribución de Goles por Posición", color_discrete_sequence=px.colors.sequential.Greys)
    figuragoles.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white")

    figuraasistencias = px.box(asistenciasxposicion, x="Posición", y="Asistencias", title="Distribución de Asistencias por Posición", color_discrete_sequence=px.colors.sequential.Greys)
    figuraasistencias.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white")

    figuradistancia = px.line(distanciaxposicion, x="Posición", y="Distancia Cubierta", title="Promedio de Distancia Cubierta por Posición", markers=True, color_discrete_sequence=px.colors.sequential.Greys)
    figuradistancia.update_layout(plot_bgcolor="black", paper_bgcolor="black", font_color="white")

    return html.Div([
        html.H1("Estadísticas por Posición", style={"textAlign": "center", "color": "white"}),
        html.P("Hola una cordial bienvendia a los dashboards esatdisticos de mi proyecto de programacion para la extraccion de datos.", style={"color": "white"}),
        html.Hr(style={"borderColor": "white"}),
        dbc.Row([
            dbc.Col(tarjetas_filtro(), width=4),
            dbc.Col([
                dcc.Graph(id="Figuragoles"),
                dcc.Graph(id="FiguraAsistencias"),
                dcc.Graph(id="Figuradistancias")
            ], width=8),
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
        return dash_layout1(df)
    elif at == "pestaña2":
        return dash_layout2()
    return html.P("This shouldn't ever be displayed...")

# Ejecutar la app
if __name__ == "__main__":
    app.run(debug=True)
