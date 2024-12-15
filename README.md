# Bitcoin Price Prediction -My Mini Project
The code has been given in my repository 
### Project Overview: Bitcoin Price Prediction with Investment Recommendation

This project is a web application that predicts the Bitcoin price for the next 7 days based on historical data. The application allows users to select a date, and it uses machine learning models (Linear Regression) to predict Bitcoin's price and provide investment recommendations (BUY, SELL, or HOLD).

### Project Breakdown:

#### 1. **Frontend (HTML and CSS) - User Interface:**
   - **HTML (`index.html`)**: 
     - The web interface is built with HTML to allow users to select a date and submit it. Upon submission, the app will display the predicted Bitcoin price for the next 7 days along with a chart and investment recommendation.
     - A **form** allows the user to select a date, which is used to trigger the prediction process when submitted.
     - Results are displayed below the form, including:
       - The **predicted Bitcoin price** for the selected date in INR.
       - A **recommendation** on whether to **BUY**, **SELL**, or **HOLD** Bitcoin based on the predicted trend.
       - An **interactive chart** showing the price prediction for the next 7 days.

   - **CSS Styling**: 
     - The design is simple and clean, with a light gradient background, a responsive container for the content, and a modern style for buttons and charts.
     - The page is styled for clarity, ensuring a pleasant user experience with readable fonts and intuitive button interactions.

#### 2. **Backend (Flask, Python) - Prediction and Analysis:**
   - **Flask Web Framework**:
     - The Flask framework is used to handle HTTP requests and render templates (`index.html`).
     - The application accepts **POST** requests when the user submits the form with a date. Upon submission, the backend processes the date and returns the prediction results.

   - **Prediction Logic**:
     - **Data Collection**: The historical Bitcoin data for the last year is fetched from the CoinGecko API. The data includes daily Bitcoin prices in INR over the last 365 days.
     - **Data Preprocessing**: The historical data is cleaned and transformed. The `day`, `month`, and `year` columns are extracted from the date to be used as features in the model.
     - **Model Training**: A Linear Regression model is trained using these date features (day, month, year) as input and the corresponding Bitcoin prices as the target output.
     - **Prediction**: For a given date, the model predicts Bitcoin prices for the next 7 days. The last predicted price is used as the predicted price for the selected date.

   - **Investment Recommendation**:
     - The predicted prices are analyzed to provide a recommendation:
       - **BUY** if the predicted prices are increasing.
       - **SELL** if the predicted prices are decreasing.
       - **HOLD** if the prices are stable.
     - This recommendation is returned along with the predicted prices.

   - **Chart Generation**:
     - **Plotly** is used to generate an interactive chart showing the predicted Bitcoin prices for the next 7 days.
     - The chart is rendered and passed to the frontend for display.

#### 3. **Machine Learning Model (Linear Regression)**:
   - A **Linear Regression model** is trained using historical Bitcoin price data. The features are the day, month, and year derived from the date, and the target variable is the Bitcoin price for that day.
   - The model is saved as `bitcoin_price_model.pkl` and loaded whenever a prediction is requested.
   - The model’s prediction is used to forecast Bitcoin prices for the next 7 days based on the input date.

#### 4. **File Structure**:
   - **`index.html`**: The main HTML file for the web interface.
   - **`prediction.py`**: The Flask Python script that handles the backend logic, including fetching historical data, training the model, and generating predictions.
   - **`bitcoin_price_model.pkl`**: The trained machine learning model file (saved after training).
   
#### 5. **Flow of the Application**:
   1. The user selects a date in the frontend form.
   2. The date is sent to the backend via a POST request.
   3. The backend:
      - Retrieves and preprocesses the historical data.
      - Trains the model if it’s the first time running the app.
      - Makes predictions for the next 7 days based on the selected date.
      - Analyzes the price trend and determines the investment action.
      - Generates an interactive chart showing the predicted Bitcoin prices.
   4. The backend sends the results, including the predicted price, recommendation, and chart, back to the frontend.
   5. The results are displayed in the browser, allowing the user to view the predictions and the investment recommendation.

#### 6. **Error Handling**:
   - If an invalid date format is entered, the application displays an error message.
   - If any other errors occur during the prediction process, the application provides a generic error message.

### Conclusion:
This project demonstrates a basic implementation of a Bitcoin price prediction model using machine learning (Linear Regression) and a web application built with Flask. It allows users to input a date, view predicted Bitcoin prices for the next 7 days, and receive investment recommendations. The interactive chart further enhances the user experience, making it visually appealing and easy to interpret the predicted data.

### OUTPUT:

![image](https://github.com/user-attachments/assets/b4c0fd65-f9cf-4871-93a1-a885c9a34164)

![image](https://github.com/user-attachments/assets/685e0e4c-b0a3-49dd-8136-17a1ff5bf10e)
![image](https://github.com/user-attachments/assets/261b19dd-ede8-4b9b-bc30-4862660db19b)
