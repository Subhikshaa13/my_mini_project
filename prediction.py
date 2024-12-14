import os
import requests
import numpy as np
from flask import Flask, render_template, request
from datetime import datetime, timedelta
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import joblib
import pandas as pd

app = Flask(__name__)

# Fetch historical Bitcoin data
def fetch_historical_data():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {'vs_currency': 'inr', 'days': '365', 'interval': 'daily'}
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract price and dates
    prices = data['prices']
    dates = [datetime.fromtimestamp(item[0] / 1000) for item in prices]
    price_values = [item[1] for item in prices]
    
    # Return as pandas DataFrame
    return pd.DataFrame({'date': dates, 'price': price_values})

# Preprocess data and train model
def train_model():
    df = fetch_historical_data()
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    # Features: day, month, year
    X = df[['day', 'month', 'year']]
    y = df['price']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Save the trained model
    joblib.dump(model, 'bitcoin_price_model.pkl')

# Load the trained model
def load_model():
    return joblib.load('bitcoin_price_model.pkl')

# Generate predictions for the next 7 days
def get_predictions(start_date):
    model = load_model()
    
    prediction_dates = [start_date + timedelta(days=i) for i in range(7)]
    
    # Prepare data for prediction (based on date features)
    prediction_features = []
    for date in prediction_dates:
        day = date.day
        month = date.month
        year = date.year
        prediction_features.append([day, month, year])

    # Predict prices
    predicted_prices = model.predict(prediction_features)
    
    return prediction_dates, predicted_prices

# Analyze predicted trend to recommend investment action (Buy, Sell, Hold)
def analyze_investment_action(predicted_prices):
    if predicted_prices[-1] > predicted_prices[0]:
        if predicted_prices[-1] - predicted_prices[0] > 5000:  # Adjust threshold as needed
            return "Buy", "The price is predicted to increase significantly. It might be a good time to buy."
        else:
            return "Hold", "The price is predicted to rise slowly. Consider holding."
    elif predicted_prices[-1] < predicted_prices[0]:
        if predicted_prices[0] - predicted_prices[-1] > 5000:  # Adjust threshold as needed
            return "Sell", "The price is predicted to drop significantly. It might be a good time to sell."
        else:
            return "Hold", "The price is predicted to decrease slowly. Consider holding."
    else:
        return "Hold", "The price is expected to stay stable. It's best to hold."

# Function to create a Plotly graph
def generate_interactive_chart(dates, prices):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines+markers', name='Predicted Price',
                             hovertemplate='<b>Date</b>: %{x}<br><b>Price</b>: ₹%{y}<extra></extra>'))

    fig.update_layout(
        title="Bitcoin Price Prediction (Next 7 Days)",
        xaxis_title="Date",
        yaxis_title="Price (INR)",
        hovermode="x unified",  # Display all info in a single hover
        template="plotly",  # White theme for the graph
        plot_bgcolor='white',  # Set the background to white
        paper_bgcolor='white',  # Set the paper background to white
        font=dict(color='black')  # Set font color to black for better contrast
    )

    # Convert the figure to HTML for embedding
    return fig.to_html(full_html=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendation = ""
    predicted_price_inr = None
    selected_date = None
    chart_html = None
    action = None  # To hold the investment action (Buy/Sell/Hold)

    if request.method == 'POST':
        # Get the date input from the user
        date_str = request.form.get('date')  # Expected format: 'YYYY-MM-DD'
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            # Handle invalid date format
            return render_template('index.html', error_message="Please provide a valid date in 'YYYY-MM-DD' format.")

        # Fetch historical data and generate predictions
        try:
            prediction_dates, predicted_prices = get_predictions(selected_date)

            # Assume the last predicted price as the predicted price for the selected date
            predicted_price_inr = predicted_prices[-1]

            # Get investment recommendation and action based on the trend
            action, recommendation = analyze_investment_action(predicted_prices)

            # Generate the interactive chart
            chart_html = generate_interactive_chart(prediction_dates, predicted_prices)
        except Exception as e:
            # Handle any errors during prediction generation
            return render_template('index.html', error_message=f"An error occurred: {str(e)}")

        return render_template('index.html',
                               predicted_price_inr=predicted_price_inr,
                               selected_date=selected_date,
                               recommendation=recommendation,
                               action=action,  # Add investment action (Buy/Sell/Hold)
                               chart_html=chart_html)
    
    return render_template('index.html')

if __name__ == '__main__':
    # First-time model training (if needed)
    if not os.path.exists('bitcoin_price_model.pkl'):
        train_model()

    app.run(debug=True)