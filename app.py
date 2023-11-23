import numpy as np
import plotly.express as px
import yfinance as yf
import datetime

app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("Dashboard de Acciones"),

    dcc.Dropdown(
        id='stocks',
        options=[{'label': stock, 'value': stock} for stock in stocks],
        value=stocks[0],
        multi=False
    ),

    # Gráfico de precios
    dcc.Graph(id='price-chart'),

    # Gráfico de retornos
    dcc.Graph(id='returns-chart'),

    # Rango de fechas
    dcc.RangeSlider(
        id='date-slider',
        min=0,
        max=len(data) - 1,
        step=1,
        marks={i: str(start + datetime.timedelta(days=i))[:10] for i in range(0, len(data), len(data) // 6)},
        value=[0, len(data) - 1],
    )
])

server=app.server
@app.callback(
    [Output('price-chart', 'figure'),
     Output('returns-chart', 'figure')],
    [Input('stocks', 'value'),
     Input('date-slider', 'value')]
)
def update_charts(selected_stock, selected_dates):
    start_date, end_date = selected_dates

    # Gráfico de precios
    price_chart = {
        'data': [
            {'x': data.index, 'y': data[selected_stock], 'type': 'line', 'name': selected_stock},
        ],
        'layout': {
            'title': f'Precio de {selected_stock}',
            'xaxis': {'title': 'Fecha'},
            'yaxis': {'title': 'Precio'},
            'xaxis_rangeslider_visible': True,  
        }
    }

    # Gráfico de retornos
    returns_chart = {
        'data': [
            {'x': returnos.index, 'y': returnos[selected_stock], 'type': 'line', 'name': f'Retornos de {selected_stock}'},
        ],
        'layout': {
            'title': f'Retornos de {selected_stock}',
            'xaxis': {'title': 'Fecha'},
            'yaxis': {'title': 'Retornos'},
            'xaxis_rangeslider_visible': True,  
        }
    }

    return price_chart, returns_chart


if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=10000)
