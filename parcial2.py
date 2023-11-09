from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

server=app.server

#Establecer carperta donde va a guardar el archivo. 
options=webdriver.ChromeOptions()
prefs={"download.default_directory":r"/Users/juanhernandez/Desktop/python"}
options.add_experimental_option("prefs",prefs)

s=Service("/Users/juanhernandez/Desktop/python/chromedriver-mac-x64/chromedriver")
driver=webdriver.Chrome(service=s,options=options)
driver.get("https://www.banguat.gob.gt/tipo_cambio/")

date=datetime(2023,1,1)
date
d=date.strftime("%d/%m/%y")
d

#inspeccionar el codigo html de la pagina y buscar el xpath de los filtros
driver.find_element("xpath",
                    "/html/body/div[1]/div/div/div/form[3]/table/tbody/tr[2]/td/div[1]/div/div[2]/div/input").clear()
driver.find_element("xpath",
                    "/html/body/div[1]/div/div/div/form[3]/table/tbody/tr[2]/td/div[1]/div/div[2]/div/input").click()
driver.find_element("xpath",
                    "/html/body/div[1]/div/div/div/form[3]/table/tbody/tr[2]/td/div[1]/div/div[2]/div/input").send_keys(d)

#Consultar la informacion
driver.find_element("xpath",
                    "/html/body/div[1]/div/div/div/form[3]/table/tbody/tr[2]/td/div[2]/div/input").click()

#Descargar la informacion
driver.find_element("xpath","/html/body/div/div/div/button").click()

#Tipo de cambio 
tp=pd.read_csv("/Users/juanhernandez/Desktop/python/histórico_rango-2.csv")
tp

#Inflacion
INF=pd.read_csv("/Users/juanhernandez/Desktop/python/sr005.csv")
INF

#PIB
PIB=pd.read_csv("/Users/juanhernandez/Desktop/python/5._PIB_per_capita.csv")
PIB

import plotly as pl
import plotly.express as px
import numpy as np
import pandas as pd

graph = px.line(tp, x="Fecha", y="TCR 1/", line_shape="linear")

tp['Fecha'] = pd.to_datetime(tp['Fecha'], format='%d/%m/%y')

tp_monthly = tp.resample('M', on='Fecha').mean()




app3 = dash.Dash(__name__)

app3.layout = html.Div([
    html.H1("Tipo de Cambio"),
    
dcc.DatePickerRange(
        id="date-range-picker",
        start_date=tp["Fecha"].min(),
        end_date=tp["Fecha"].max(),
        display_format="D/M/YY",
        minimum_nights=0,  
    ),
    # Graph
    dcc.Graph(id="time-series-graph", figure=graph),
])

@app3.callback(
    Output("time-series-graph", "figure"),
    Input("date-range-picker", "start_date"),
    Input("date-range-picker", "end_date")
)
def update_graph(start_date, end_date):
    filtered_data = tp_monthly[(tp_monthly.index >= start_date) & (tp_monthly.index <= end_date)]
    updated_graph = px.line(filtered_data, x=filtered_data.index, y="TCR 1/", line_shape="linear")
    return updated_graph


if __name__ == "__main__":
    app3.run_server(port=2240, debug=False)


#Grafica interactiva del Comportamiento del tipo de cambio este año
graph=px.line(tp,x="Fecha",y="TCR 1/",
             line_shape="linear")
graph

from dash import Dash,dcc,html,Input,Output

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime

variables = list(INF.columns)

INF["Fecha"] = pd.to_datetime(INF["Fecha"], format="%d/%m/%y")


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Inflacion"),
    
 
    dcc.Dropdown(
        id="variableSelector",
        options=[{'label': variable, 'value': variable} for variable in variables],
        value=variables[0]  
    ),

 
    dcc.DatePickerRange(
        id="dateRangeSelector",
        start_date=INF['Fecha'].min(),  
        end_date=INF['Fecha'].max(),    
    ),
    
    
    dcc.Graph(id="line-plot"),
    
    
    dcc.Graph(id="scatter-plot")
])


@app.callback(
    Output("line-plot", "figure"),
    Output("scatter-plot", "figure"),
    [Input("variableSelector", "value"),
     Input("dateRangeSelector", "start_date"),
     Input("dateRangeSelector", "end_date")]
)
def update_plots(selected_variable, start_date, end_date):
    filtered_data = INF[(INF['Fecha'] >= start_date) & (INF['Fecha'] <= end_date)]
        
    
    line_fig = px.line(filtered_data, x="Fecha", y=selected_variable, title=f"{selected_variable} - Line Plot")

    
    scatter_fig = px.scatter(filtered_data, x="Fecha", y=selected_variable, title=f"{selected_variable} - Scatter Plot")
    
    return line_fig, scatter_fig


if __name__ == "__main__":
    app.run_server(debug=False,host="0.0.0.0",port=10000)

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_table


data = {
    "AÑO": [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    "PIB per cápita en quetzales b/": [27677.7, 29225.0, 30578.1, 31716.7, 32727.9, 33729.1, 35772.8, 35596.0, 38899.9, 42407.8],
    "Tasa de Variación": [None, 5.6, 4.6, 3.7, 3.2, 3.1, 6.1, -0.5, 9.3, 9.0],
    "PIB per cápita en US dólares": [3522.9, 3780.3, 3994.2, 4172.1, 4452.3, 4485.8, 4646.8, 4609.6, 5028.6, 5472.8],
    "Tasa de Variación.1": [None, 7.3, 5.7, 4.5, 6.7, 0.8, 3.6, -0.8, 9.1, 8.8]
}

PIB = pd.DataFrame(data)

app = dash.Dash(__name__)

table = dash_table.DataTable(
    columns=[{"name": i, "id": i} for i in PIB.columns],
    data=PIB.to_dict("records"),
    export_format="csv",
    fill_width=True,
    style_header={'backgroundColor': 'blue', 'color': 'white'},
)

app.layout = html.Div([
    html.H1("PIB Dashboard"),
    
    dcc.Dropdown(
        id="variableSelector",
        options=[{'label': variable, 'value': variable} for variable in PIB.columns[1:]],
        value="PIB per cápita en quetzales b/"
    ),

    dcc.RangeSlider(
        id="dateRangeSelector",
        min=PIB["AÑO"].min(),
        max=PIB["AÑO"].max(),
        step=1,
        marks={year: str(year) for year in PIB["AÑO"]},
        value=[PIB["AÑO"].min(), PIB["AÑO"].max()]
    ), 
    
    
    dcc.Graph(id="bar-chart"),
    
    
    dcc.Graph(id="line-chart"),
    
     html.Div([
        html.H2("Table"),
        table
    ])
])

    
@app.callback(
    Output("bar-chart", "figure"),
    Output("line-chart", "figure"),
    [Input("variableSelector", "value"),
     Input("dateRangeSelector", "value")]
)
def update_plots(selected_variable, date_range):
    start_year, end_year = date_range
    filtered_data = PIB[(PIB["AÑO"] >= start_year) & (PIB["AÑO"] <= end_year)]
    
    bar_fig = px.bar(filtered_data, x="AÑO", y=selected_variable, title=f"{selected_variable} - Bar Chart")
    line_fig = px.line(filtered_data, x="AÑO", y=selected_variable, title=f"{selected_variable} - Line Chart")
    
    
    return bar_fig, line_fig



if __name__ == "__main__":
    app.run_server(debug=False,host="0.0.0.0",port=10000)
    


