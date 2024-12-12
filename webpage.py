import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import re
# Load and preprocess the dataset
df = pd.read_csv('sentiment.csv').copy()
df = df.sort_values(by='Date')
df['Compound'] = df['Positive'] - df['Negative']
df.rename(columns={
    'Date': 'Date',
    'Stock': 'Stock',
    'Open Price': 'Stock Price',
    'Articles': 'Articles',
    'Positive': 'Positive Sentiment',
    'Neutral': 'Neutral Sentiment',
    'Negative': 'Negative Sentiment'
}, inplace=True)

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Drop rows with missing values
df.dropna(subset=['Stock Price', 'Positive Sentiment', 'Neutral Sentiment', 'Negative Sentiment'], inplace=True)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Stock Prices and Sentiment Analysis Dashboard", 
            style={
                'text-align': 'center', 
                'color': '#ffffff', 
                'padding': '20px 0', 
                'font-family': 'Poppins, sans-serif',
                'font-size': '36px',
                'font-weight': '600',
                'background': 'linear-gradient(45deg, #f39c12, #e74c3c)',
                'border-radius': '8px',
                'box-shadow': '0 4px 10px rgba(0, 0, 0, 0.3)'
            }),

    # Filters
    html.Div(
        [
            html.H2("Dashboard Overview", style={'text-align': 'center', 'margin-bottom': '15px'}),
            html.P(
                "Our purpose is to investigate the relationship between news and social media sentiment and stock market volatility, uncovering meaningful patterns in public sentiment to forecast stock movements and market trends. The dashboard includes three key visualizations:"
                "1.⁠ ⁠A *line chart* displaying stock prices over time with sentiment thresholds.  "
                "2.⁠ ⁠A *bar chart* summarizing the sentiment composition for a selected stock and date range. " 
                "3.⁠ ⁠A *compound sentiment chart* showing overall sentiment trends over time.  "

                "The sentiment chart now includes additional interactivity. By clicking on a specific *month and year* in the overall sentiment chart, a dynamic dashboard appears at the bottom, displaying detailed metrics for all tracked stocks. These include the selected stock's *date, name, average open price, average close price, and monthly percentage change*, along with any other relevant metrics available in the dataset. " 

                "Additionally, a new feature allows you to plot the *price trend line for a stock over time* directly on the sentiment chart.  "

                "Use the interactive filters to explore the data, analyze sentiment-driven stock trends, and uncover actionable insights.",
                style={
                    'text-align': 'justify',
                    'font-size': '16px',
                    'margin': '0 auto',
                    'max-width': '900px',
                    'color': '#333',
                    'line-height': '1.6'
                }
            ),
        ],
        style={
            'padding': '20px',
            'background-color': '#f9f9f9',
            'border-radius': '8px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'margin-bottom': '30px'
        }
    ),
    html.Div([
        html.Div([
            html.Label("Select Stock:", style={'font-weight': '600', 'font-size': '14px', 'color': '#34495e'}),
            dcc.Dropdown(
                id='stock-dropdown',
                options=[{'label': stock, 'value': stock} for stock in df['Stock'].unique()],
                value=df['Stock'].unique()[0],
                clearable=False
            )
        ], style={
            'width': '22%', 
            'display': 'inline-block', 
            'padding': '10px', 
            'margin-right': '3%',
            'background-color': '#3498db', 
            'border-radius': '8px',
            'box-shadow': '0 4px 12px rgba(0, 0, 0, 0.2)',
            'transition': 'all 0.3s ease',
            'cursor': 'pointer'
        }),

        html.Div([
            html.Label("Select Sentiment Type:", style={'font-weight': '600', 'font-size': '14px', 'color': '#34495e'}),
            dcc.Dropdown(
                id='sentiment-dropdown',
                options=[
                    {'label': 'Positive', 'value': 'Positive Sentiment'},
                    {'label': 'Neutral', 'value': 'Neutral Sentiment'},
                    {'label': 'Negative', 'value': 'Negative Sentiment'},
                    {'label': 'All', 'value': 'All Sentiments'}
                ],
                value='All Sentiments',
                clearable=False
            )
        ], style={
            'width': '22%', 
            'display': 'inline-block', 
            'padding': '10px', 
            'margin-right': '3%',
            'background-color': '#e67e22', 
            'border-radius': '8px',
            'box-shadow': '0 4px 12px rgba(0, 0, 0, 0.2)',
            'transition': 'all 0.3s ease',
            'cursor': 'pointer'
        }),

        html.Div([
            html.Label("Select Sentiment Threshold:", style={'font-weight': '600', 'font-size': '14px', 'color': '#34495e'}),
            dcc.Slider(
                id='threshold-slider',
                min=0,
                max=1,
                step=0.01,
                value=0.7,
                marks={i/10: f'{i/10}' for i in range(0, 11)},
                tooltip={'placement': 'bottom', 'always_visible': True}
            )
        ], style={
            'width': '22%', 
            'display': 'inline-block', 
            'padding': '10px', 
            'margin-right': '3%',
            'background-color': '#1abc9c', 
            'border-radius': '8px',
            'box-shadow': '0 4px 12px rgba(0, 0, 0, 0.2)',
            'transition': 'all 0.3s ease',
            'cursor': 'pointer'
        }),

        html.Div([
            html.Label("Select Date Range:", style={'font-weight': '600', 'font-size': '14px', 'color': '#34495e'}),
            dcc.DatePickerRange(
                id='date-picker',
                start_date=df['Date'].min(),
                end_date=df['Date'].max(),
                display_format='YYYY-MM-DD'
            )
        ], style={
            'width': '22%', 
            'display': 'inline-block', 
            'padding': '10px', 
            'background-color': '#9b59b6', 
            'border-radius': '8px',
            'box-shadow': '0 4px 12px rgba(0, 0, 0, 0.2)',
            'transition': 'all 0.3s ease',
            'cursor': 'pointer'
        })
    ], style={
        'display': 'flex', 
        'justify-content': 'space-between', 
        'align-items': 'center', 
        'background-color': '#ecf0f1', 
        'border-radius': '10px', 
        'padding': '15px 20px',
        'margin-bottom': '30px'
    }),
    
    # Charts
    html.Div([
        html.Div(id='headline-output', style={'margin-top': '20px', 'font-size': '18px', 'font-weight': '600'}),        
        dcc.Graph(id='line-chart', style={'margin-bottom': '30px'}),
        dcc.Graph(id='compound-sentiment-chart', style={'margin-bottom': '30px'}),
        html.Div(id='price-info', style={'fontSize': 20, 'marginTop': 20}),
        dcc.Graph(id='sentiment-composition-chart', style={'margin-bottom': '30px'}),

])

], style={
    'margin': '0 auto', 
    'max-width': '1200px', 
    'padding': '40px', 
    'background-color': '#ffffff', 
    'border-radius': '10px', 
    'box-shadow': '0 8px 20px rgba(0, 0, 0, 0.2)',
    'transition': 'all 0.5s ease-in-out',
})

@app.callback(
    Output('line-chart', 'figure'),
    [
        Input('stock-dropdown', 'value'),
        Input('sentiment-dropdown', 'value'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
        Input('threshold-slider', 'value')
    ]
)
def update_graphs(selected_stock, selected_sentiment, start_date, end_date, threshold):
    # Filter the dataframe based on stock and date range
    filtered_df = df[(df['Stock'] == selected_stock) &
                     (df['Date'] >= start_date) &
                     (df['Date'] <= end_date)].copy()

    # Create a new column for Threshold mapping
    filtered_df['Threshold'] = 'Neutral'  # Default to Neutral

    # Apply threshold filtering based on sentiment type
    if selected_sentiment != 'All Sentiments':
        filtered_df = filtered_df[filtered_df[selected_sentiment] >= threshold]
        filtered_df['Threshold'] = selected_sentiment.split()[0]
    else:
        filtered_df['Threshold'] = filtered_df[['Positive Sentiment', 'Neutral Sentiment', 'Negative Sentiment']].idxmax(axis=1).str.split().str[0]

    # Line Chart for stock prices
    line_chart = go.Figure()

    # Add stock price line for the entire period (only once)
    line_chart.add_trace(go.Scatter(
        x=df[(df['Stock'] == selected_stock) & (df['Date'] >= start_date) & (df['Date'] <= end_date)]['Date'],
        y=df[(df['Stock'] == selected_stock) & (df['Date'] >= start_date) & (df['Date'] <= end_date)]['Stock Price'],
        mode='lines',
        name='Stock Price',
        line=dict(color='black')
    ))

    # Add sentiment markers
    line_chart.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['Stock Price'],
        mode='markers',
        name='Sentiment Threshold',
        marker=dict(
            color=filtered_df['Threshold'].map({'Positive': '#2ecc71', 'Neutral': '#3498db', 'Negative': '#e74c3c'}),
            size=12, opacity=0.8
        )
    ))

    line_chart.update_layout(
        title="Stock Prices and Sentiment Over Time",
        xaxis_title="Date",
        yaxis_title="Stock Price",
        legend_title="Metric",
        font=dict(family="Arial, sans-serif", size=14),
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='#f9f9f9',
        plot_bgcolor='#f9f9f9'
    )

    return line_chart
    
@app.callback(
    [
        Output('compound-sentiment-chart', 'figure'),
        Output('price-info', 'children')  # New Output to display price info
    ],
    [
        Input('stock-dropdown', 'value'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
        Input('compound-sentiment-chart', 'clickData')  # Capture the click data
    ]
)
def update_compound_sentiment_graph(selected_stock, start_date, end_date, clickData):
    # Filter the dataframe based on stock and date range
    filtered_df = df[(df['Stock'] == selected_stock) & 
                     (df['Date'] >= start_date) & 
                     (df['Date'] <= end_date)].copy()
    
    # Ensure 'Date' is a datetime type
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    
    # Resample to monthly data for compound sentiment
    aggregated_sentiment_df = filtered_df.resample('ME', on='Date')['Compound'].sum().reset_index()
    
    # Resample to monthly data for open price
    aggregated_price_df = filtered_df.resample('ME', on='Date')['Stock Price'].first().reset_index()
    aggregated_price_df['PctChange'] = aggregated_price_df['Stock Price'].pct_change() * 100  # Percentage change

    # Apply scaling to PctChange (e.g., Min-Max Scaling to range [0, 1])
    pct_change_min = aggregated_price_df['PctChange'].min()
    pct_change_max = aggregated_price_df['PctChange'].max()

    # Avoid division by zero in case all changes are the same
    if pct_change_max - pct_change_min > 0:
        aggregated_price_df['ScaledPctChange'] = (aggregated_price_df['PctChange'] - pct_change_min) / (pct_change_max - pct_change_min)
    else:
        aggregated_price_df['ScaledPctChange'] = 0  # All values are the same, scale to 0

    # Create the compound sentiment line chart
    compound_sentiment_chart = go.Figure()

    # Add the compound sentiment line
    compound_sentiment_chart.add_trace(go.Scatter(
        x=aggregated_sentiment_df['Date'],
        y=aggregated_sentiment_df['Compound'],
        mode='lines',
        name='Compound Sentiment',
        line=dict(color='#9b59b6')
    ))

    # Add the scaled open price percentage change line
    compound_sentiment_chart.add_trace(go.Scatter(
        x=aggregated_price_df['Date'],
        y=aggregated_price_df['ScaledPctChange'],
        mode='lines+markers',
        name='Scaled Open Price % Change',
        line=dict(color='#3498db'),
        yaxis='y2'
    ))

    # Update layout to include a secondary y-axis
    compound_sentiment_chart.update_layout(
        title="Overall Sentiment (Compound Score) and Scaled Open Price % Change By Month",
        xaxis_title="Month",
        yaxis=dict(title="Compound Sentiment"),
        yaxis2=dict(
            title="Scaled Open Price % Change",
            overlaying='y',
            side='right'
        ),
        legend_title="Metric",
        font=dict(family="Arial, sans-serif", size=14),
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='#f9f9f9',
        plot_bgcolor='#f9f9f9'
    )

    price_info = []
    if clickData:
        clicked_date = clickData['points'][0]['x']
        clicked_price = aggregated_price_df[aggregated_price_df['Date'] == clicked_date]['Stock Price'].values[0]
        pct_change = aggregated_price_df[aggregated_price_df['Date'] == clicked_date]['PctChange'].values[0]
        
        color = 'green' if pct_change >= 0 else 'red'
        
        price_info = [
            html.H3("Price Information", style={'fontFamily': 'Helvetica, Arial, sans-serif', 'marginBottom': '10px'}),
            html.P(f"Price: ${clicked_price:.2f}", style={'fontFamily': 'Helvetica, Arial, sans-serif', 'marginBottom': '5px'}),
            html.P([
                "Percent Change: ",
                html.Span(f"{pct_change:+.2f}%", style={'color': color, 'fontWeight': 'bold'})
            ], style={'fontFamily': 'Helvetica, Arial, sans-serif'})
        ]
    
    return compound_sentiment_chart, price_info
@app.callback(
    Output('sentiment-composition-chart', 'figure'),
    [
        Input('stock-dropdown', 'value'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date')
    ]
)
def update_sentiment_composition(selected_stock, start_date, end_date):
    # Filter the dataframe based on stock and date range
    filtered_df = df[(df['Stock'] == selected_stock) & 
                     (df['Date'] >= start_date) & 
                     (df['Date'] <= end_date)]

    # Aggregate sentiment scores
    sentiment_summary = filtered_df[['Positive Sentiment', 'Neutral Sentiment', 'Negative Sentiment']].mean()

    # Create a bar chart for sentiment composition
    sentiment_composition_chart = go.Figure(data=[
        go.Bar(
            x=['Positive', 'Neutral', 'Negative'],
            y=sentiment_summary,
            text=sentiment_summary.round(2),
            textposition='auto',
            marker_color=['#2ecc71', '#3498db', '#e74c3c']
        )
    ])

    sentiment_composition_chart.update_layout(
        title="Sentiment Composition for Selected Stock and Date Range",
        xaxis_title="Sentiment Type",
        yaxis_title="Average Sentiment Score",
        font=dict(family="Arial, sans-serif", size=14),
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='#f9f9f9',
        plot_bgcolor='#f9f9f9',
        showlegend=False
    )

    return sentiment_composition_chart

@app.callback(
    Output('headline-output', 'children'),
    [
        Input('line-chart', 'clickData'),
        Input('stock-dropdown', 'value'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date')
    ]
)
def display_headline(clickData, selected_stock, start_date, end_date):
    if clickData is None:
        return html.Div(
            "Select a sentiment point to view the headline.",
            style={
                'font-size': '18px', 
                'font-weight': '600',
                'color': '#7f8c8d',
                'text-align': 'center',
                'margin-top': '20px',
                'font-family': 'Poppins, sans-serif'
            }
        )
    
    # Extract the date of the selected sentiment point
    selected_date = clickData['points'][0]['x']
    
    # Find the corresponding article for that date
    articles = df[(df['Stock'] == selected_stock) & 
                  (df['Date'] == pd.to_datetime(selected_date))]['Articles'].values
    pattern = r"Headline:\s*(.*?)(?=\s*,|\Z)"  # Updated regex pattern

    headlines = [re.search(pattern, article).group(1) for article in articles]

    if headlines:
        return html.Div(
            f"Date: {selected_date} - {headlines[0]}",
            style={
                'font-size': '22px',
                'font-weight': '600',
                'color': '#2c3e50',
                'background-color': '#ecf0f1',
                'padding': '15px',
                'border-radius': '8px',
                'box-shadow': '0 4px 12px rgba(0, 0, 0, 0.2)',
                'margin-top': '20px',
                'font-family': 'Poppins, sans-serif',
                'transition': 'all 0.3s ease-in-out'
            }
        )
    else:
        return html.Div(
            "No headline available for the selected date.",
            style={
                'font-size': '18px', 
                'font-weight': '600',
                'color': '#e74c3c',
                'text-align': 'center',
                'margin-top': '20px',
                'font-family': 'Poppins, sans-serif'
            }
        )

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
