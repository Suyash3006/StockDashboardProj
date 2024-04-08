import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(style={'backgroundImage': 'linear-gradient(to bottom, #000000, #130f40)', 'padding': '30px', 'margin': '-20px'}, children=[
    html.Div(style={'display': 'flex', 'align-items': 'flex-start', 'marginBottom': '20px'}, children=[
        html.Img(src='https://cdn-icons-png.freepik.com/512/4953/4953605.png', style={'height': '100px', 'width': 'auto', 'marginRight': '20px'}),
        html.H1("Stock Price Analysis Dashboard", 
                style={'textAlign': 'center', 
                       'color': '#ffffff', 
                       'fontFamily': 'Arial, sans-serif',
                       'cursor': 'pointer',
                       'transition': 'color 0.5s',
                       'fontWeight': 'normal',
                       'fontSize': '36px',
                       'marginTop': '20px',
                       'marginBottom': '0px'},
                id='heading'
               ),
    ]),
    
    # Dropdown for selecting stock symbol
    html.Label("Select Stock Symbol", style={'color': '#ffffff', 'marginTop': '20px' , 'font-size' : '20px'}),
    dcc.Dropdown(
        id='stock-dropdown',
        options=[
            {'label': 'Apple Inc. (AAPL)', 'value': 'AAPL'},
            {'label': 'Microsoft Corporation (MSFT)', 'value': 'MSFT'},
            {'label': 'Amazon.com Inc. (AMZN)', 'value': 'AMZN'},
            {'label': 'Alphabet Inc. (GOOGL)', 'value': 'GOOGL'},
            {'label': 'Facebook, Inc. (FB)', 'value': 'FB'},
            {'label': 'Tesla, Inc. (TSLA)', 'value': 'TSLA'},
            {'label': 'NVIDIA Corporation (NVDA)', 'value': 'NVDA'},
            {'label': 'PayPal Holdings, Inc. (PYPL)', 'value': 'PYPL'},
            {'label': 'Netflix, Inc. (NFLX)', 'value': 'NFLX'},
            {'label': 'Zoom Video Communications, Inc. (ZM)', 'value': 'ZM'},
        ],
        value='AAPL',
        multi=False,
        style={'width' : '40%' , 'backgroundColor': 'lightgrey', 'color': '#a9a9a9' , 'margin-top' : '20px'}
    ),
    
    # Date range picker
    html.Label("Select Date Range", style={'color': '#ffffff', 'margin-top': '20px' , 'font-size' : '20px'}),
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed='2015-01-01',
        max_date_allowed='2022-01-01',
        start_date='2021-01-01',
        end_date='2022-01-01',
        style={'margin-left': '30px','margin-top' : '30px',  'font-size': '10px'}
    ),

    
    # Select Plot Type
    html.Div([
        html.Label("Select Plot Type", style={'color': '#ffffff', 'display': 'inline-block' ,'margin-top': '20px' , 'font-size' : '20px'}),
        dcc.RadioItems(
            id='plot-type',
            options=[
                {'label': 'Candlestick Chart', 'value': 'candlestick'},
                {'label': 'Line Chart', 'value': 'line'},
            ],
            value='candlestick',
            labelStyle={'display': 'inline-block', 'margin-right': '10px' ,'margin-top': '20px' , 'color' : 'white' , 'margin-left' : '20px' , 'margin-bottom' : '20px'}
        )
    ]),
    
    # Color picker for selecting color scheme
    html.Label("Select Color Scheme", style={'color': '#ffffff' , 'font-size': '20px'}),
    dcc.Dropdown(
        id='color-scheme',
        options=[
            {'label': 'Blue and Orange', 'value': 'blue_orange'},
            {'label': 'Green and Red', 'value': 'green_red'},
            {'label': 'Purple and Yellow', 'value': 'purple_yellow'},
            {'label': 'Black and White', 'value': 'black_white'},
            {'label': 'Pink and Gray', 'value': 'pink_gray'},
            {'label': 'Teal and Brown', 'value': 'teal_brown'},
            {'label': 'Cyan and Magenta', 'value': 'cyan_magenta'},
            {'label': 'Navy Blue and Gold', 'value': 'navy_gold'},
            {'label': 'Turquoise and Coral', 'value': 'turquoise_coral'},
        ],
        value='green_red',
        multi=False,
        style={'width' : '40%','backgroundColor': 'lightgrey', 'color': '#a9a9a9' , 'margin-top' : '20px' , 'margin-bottom' : '20px' , 'padding-right' : '5px'}
    ),
    
    # Slider for selecting moving average interval
    # Slider for selecting moving average interval
    
    html.Label("Moving Average Interval", style={'color': '#ffffff' , 'font-size' : '20px'}),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Slider(
        id='moving-average-interval',
        min=1,
        max=30,
        step=1,
        value=10,
        marks={i: str(i) for i in range(1, 31)},
        className='slider-style'
    ),


    
    # Radio items for selecting duration
    html.Br(),
    html.Br(),
    html.Label("Select Duration", style={'color': '#ffffff' , 'font-size' : '20px'}),
    dcc.RadioItems(
        id='duration-radio',
        options=[
            {'label': '1 Day', 'value': '1d'},
            {'label': '1 Week', 'value': '1wk'},
            {'label': '1 Month', 'value': '1mo'}
        ],
        value='1d',
        labelStyle={'display': 'inline-block', 'margin-right': '10px' , 'margin-top' : '20px' , 'color': '#ffffff' , 'margin-bottom' : '20px'}
    ),
    
    # Output for displaying stock price plots
    dcc.Graph(id='stock-price-plot'),
    
    # Pie chart for different stock values
    html.Div([
        dcc.Graph(id='pie-chart')
    ] , style={'position': 'absolute', 'top': '20px', 'right': '20px' ,'backgroundColor': 'linear-gradient(to bottom, #000000, #130f40)'}),
    
    # Bar chart for earnings comparison
    html.Div([
        dcc.Graph(id='earnings-bar-chart')
    ])
])

# Callback function to update stock price plot, pie chart, and earnings comparison bar chart
@app.callback(
    [Output('stock-price-plot', 'figure'),
     Output('pie-chart', 'figure'),
     Output('earnings-bar-chart', 'figure')],
    [Input('stock-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('plot-type', 'value'),
     Input('color-scheme', 'value'),
     Input('moving-average-interval', 'value'),
     Input('duration-radio', 'value')]
)
def update_stock_charts(stock_symbol, start_date, end_date, plot_type, color_scheme, moving_average_interval, duration):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date, interval=duration)
    
    #candlestick or line plot based on selection
    if plot_type == 'candlestick':
        trace = go.Candlestick(
            x=stock_data.index,
            open=stock_data['Open'],
            high=stock_data['High'],
            low=stock_data['Low'],
            close=stock_data['Close'],
            name='Candlestick',
            increasing_line_color=color_scheme.split('_')[0],
            decreasing_line_color=color_scheme.split('_')[1]
        )
    elif plot_type == 'line':
        trace = go.Scatter(
            x=stock_data.index,
            y=stock_data['Close'],
            mode='lines',
            name='Closing Price',
            line=dict(color=color_scheme.split('_')[0])
        )
    
    # Add moving average line
    stock_data['Moving_Avg'] = stock_data['Close'].rolling(window=moving_average_interval).mean()
    moving_average_trace = go.Scatter(
        x=stock_data.index,
        y=stock_data['Moving_Avg'],
        mode='lines',
        name=f'{moving_average_interval}-Day Moving Average',
        line=dict(color=color_scheme.split('_')[1])
    )
    
    # Create layout for the stock price plot
    stock_layout = go.Layout(
        title=f"{stock_symbol} Stock Price Analysis",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Price"),
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#ffffff')
    )
    
    # Combine trace and moving average plot for the stock price plot
    stock_figure = go.Figure(data=[trace, moving_average_trace], layout=stock_layout)
    
    # Create pie chart data
    pie_data = [go.Pie(labels=['Open', 'Close', 'High', 'Low'], 
                       values=[stock_data['Open'].mean(), 
                               stock_data['Close'].mean(), 
                               stock_data['High'].mean(), 
                               stock_data['Low'].mean()],
                       hole=0.3,
                       marker=dict(colors=['#00adb5', '#ff5722', '#ffa726', '#4caf50']))]
    
    # Create layout for the pie chart
    pie_layout = go.Layout(
        title=f"{stock_symbol} Average Stock Values",
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#ffffff')
    )
    
    # Create pie chart figure
    pie_figure = go.Figure(data=pie_data, layout=pie_layout)
    
    # Calculate earnings comparison
    earnings_comparison = stock_data['Close'] - stock_data['Open']
    
    # Create bar chart data
    bar_data = go.Bar(
        x=stock_data.index,
        y=earnings_comparison,
        marker=dict(color=color_scheme.split('_')[0])
    )
    
    # Create layout for the earnings comparison bar chart
    bar_layout = go.Layout(
        title=f"Earnings Comparison for {stock_symbol}",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Earnings"),
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#ffffff')
    )
    
    # Create earnings comparison bar chart figure
    bar_figure = go.Figure(data=[bar_data], layout=bar_layout)
    
    return stock_figure, pie_figure, bar_figure

# CSS styles for hovering over the heading
app.css.append_css({
    'external_url': (
        '''
        .slider-style .rc-slider-track {
            background-color: #303030 !important;
        }
        .slider-style .rc-slider-handle {
            background-color: #00adb5 !important;
            border-color: #00adb5 !important;
        }
        .slider-style .rc-slider-handle:hover {
            background-color: #00adb5 !important;
            border-color: #00adb5 !important;
        }
        .slider-style .rc-slider-handle:focus {
            box-shadow: 0px 0px 0px 5px rgba(0, 0, 0, 0.1) !important;
        }
        '''
    )
})

# app.css.append_css({
#     'external_url': (
#         'h1:hover {'
#         '   color: #00adb5 !important;'
#         '   font-weight: bold;'
#         '}'
#     )
# })

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
