
import dash
import dash_core_components as dcc
#from dash import dcc
import dash_html_components as html
#from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
import io
import boto3
#import dash_table

import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAXResults
#from statsmodels.formula.api import ols
import warnings
from pandas.tseries.offsets import DateOffset


import numpy as np
import pandas as pd
import datetime as dt

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Proyecto 2 ACTD"

server = app.server
app.config.suppress_callback_exceptions = True

# Load data
def load_data():

    # Credenciales para acceder a los datos en el bucket de AWS
    REGION = 'us-east-1'
    ACCESS_KEY_ID = 'AKIASGHVVXZRRSHOMVMH'
    SECRET_ACCESS_KEY = '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'
    BUCKET_NAME = 'equipomodelos-proyectoenergia'
    KEY = 'datos_forecast.csv'

    # Cargar datos
    s3c = boto3.client(
        's3', 
        region_name = REGION,
        aws_access_key_id = ACCESS_KEY_ID,
        aws_secret_access_key = SECRET_ACCESS_KEY
    )
    obj = s3c.get_object(Bucket= BUCKET_NAME , Key = KEY)
    data = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8')

    # Elegir la fecha como el index del df
    data['Unnamed: 0'] = pd.to_datetime(data['Unnamed: 0'], utc=True).dt.tz_convert('Europe/Vienna')
    data.index = data['Unnamed: 0']
    data.drop(columns=['Unnamed: 0'], inplace=True)

    return data


# Cargar datos
data = load_data()
#model = load_model("data/SARIMA11221224.pkl")


# Graficar serie
def plot_series(data, initial_date, proy):

    data_plot = data.loc[initial_date:]
    data_plot = data_plot[:-(120-proy)]
    fig = go.Figure([
        go.Scatter(
            name='Demanda energética',
            x=data_plot.index,
            y=data_plot['AT_load_actual_entsoe_transparency'],
            mode='lines',
            line=dict(color="#188463"),
        ),
        go.Scatter(
            name='Proyección',
            x=data_plot.index,
            y=data_plot['forecast'],
            mode='lines',
            line=dict(color="#bbffeb",),
        ),
        go.Scatter(
            name='Upper Bound',
            x=data_plot.index,
            y=data_plot['Upper bound'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=data_plot.index,
            y=data_plot['Lower bound'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor="rgba(242, 255, 251, 0.3)",
            fill='tonexty',
            showlegend=False
        )
    ])

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis_title='Demanda total [MW]',
        #title='Continuous, variable value error bars',
        hovermode="x"
    )
    #fig = px.line(data2, x='local_timestamp', y="Demanda total [MW]", markers=True, labels={"local_timestamp": "Fecha"})
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#2cfec1")
    fig.update_xaxes(showgrid=True, gridwidth=0.25, gridcolor='#7C7C7C')
    fig.update_yaxes(showgrid=True, gridwidth=0.25, gridcolor='#7C7C7C')
    #fig.update_traces(line_color='#2cfec1')

    return fig



def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            #html.H5("Proyecto 1"),
            html.H3("Pronóstico de producción energética"),
            html.Div(
                id="intro",
                children="Esta herramienta contiene información sobre la demanda energética total en Austria cada hora según lo públicado en ENTSO-E Data Portal. Adicionalmente, permite realizar pronósticos hasta 5 dias en el futuro."
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[

            # Fecha inicial
            html.P("Seleccionar fecha y hora inicial:"),

            html.Div(
                id="componentes-fecha-inicial",
                children=[
                    html.Div(
                        id="componente-fecha",
                        children=[
                            dcc.DatePickerSingle(
                                id='datepicker-inicial',
                                min_date_allowed=min(data.index.date),
                                max_date_allowed=max(data.index.date),
                                initial_visible_month=min(data.index.date),
                                date=max(data.index.date)-dt.timedelta(days=7)
                            )
                        ],
                        style=dict(width='30%')
                    ),
                    
                    html.P(" ",style=dict(width='5%', textAlign='center')),
                    
                    html.Div(
                        id="componente-hora",
                        children=[
                            dcc.Dropdown(
                                id="dropdown-hora-inicial-hora",
                                options=[{"label": i, "value": i} for i in np.arange(0,25)],
                                value=pd.to_datetime(max(data.index)-dt.timedelta(days=7)).hour,
                                # style=dict(width='50%', display="inline-block")
                            )
                        ],
                        style=dict(width='20%')
                    ),
                ],
                style=dict(display='flex')
            ),

            html.Br(),

            # Slider proyección
            html.Div(
                id="campo-slider",
                children=[
                    html.P("Ingrese horas a proyectar:"),
                    dcc.Slider(
                        id="slider-proyeccion",
                        min=0,
                        max=119,
                        step=1,
                        value=0,
                        #marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                    )
                ]
            )     
     
        ]
    )


app.layout = html.Div(
    id="app-container",
    children=[
        
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[


                # Grafica de la serie de tiempo
                html.Div(
                    id="model_graph",
                    children=[
                        html.B("Demanda energética total en Austria [MW]"),
                        html.Hr(),
                        dcc.Graph(
                            id="plot_series",
                        )
                    ],
                ),

            
            ],
        ),
    ],
)


@app.callback(
    Output(component_id="plot_series", component_property="figure"),
    [Input(component_id="datepicker-inicial", component_property="date"),
    Input(component_id="dropdown-hora-inicial-hora", component_property="value"),
    Input(component_id="slider-proyeccion", component_property="value")]
)
def update_output_div(date, hour, proy):

    if ((date is not None) & (hour is not None) & (proy is not None)):
        hour = str(hour)
        minute = str(0)

        initial_date = date + " " + hour + ":" + minute
        initial_date = pd.to_datetime(initial_date, format="%Y-%m-%d %H:%M").tz_localize('Europe/Vienna')

        # Graficar
        plot = plot_series(data, initial_date, int(proy))
        return plot


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
    #app.run_server(host="0.0.0.0", debug=True)