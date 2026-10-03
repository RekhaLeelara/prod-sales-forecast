import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask("Sales Forecast Predictor ")

# Load the trained Boston housing model
loaded_model = joblib.load("superkart_model.joblib")

# Define a route for the home page
@app.get('/')
def home():
    return "Welcome to the Sales Forecast Prediction API!"

# Define an endpoint to predict price for a single house
@app.post('/v1/Sales')
def predict_sales_price():
    # Get JSON data from the request
    salesprice_data = request.get_json()

    # Extract relevant house features from the input data
    sample = {
        'Product_Id': salesprice_data['Product_Id'],
        'Product_Weight': salesprice_data['Product_Weight'],
        'Product_Sugar_Content': salesprice_data['Product_Sugar_Content'],
        'Product_Allocated_Area': salesprice_data['Product_Allocated_Area'],
        'Product_Type': salesprice_data['Product_Type'],
        'Product_MRP': salesprice_data['Product_MRP'],
        'Store_Id': salesprice_data['Store_Id'],
        'Store_Establishment_Year': salesprice_data['Store_Establishment_Year'],
        'Store_Size': salesprice_data['Store_Size'],
        'Store_Location_City_Type': salesprice_data['Store_Location_City_Type'],
        'Store_Type': salesprice_data['Store_Type'],
        'Product_Store_Sales_Total': salesprice_data['Product_Store_Sales_Total']
    }
    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Predicted_Product_Store_Sales_Total': prediction})

# Define an endpoint to predict price for a batch of Products
@app.post('/v1/salesforecast')
def predict_house_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # Add predictions to the DataFrame
    input_data['Predicted_Product_Store_Sales_Total'] = predictions

    # Convert results to dictionary
    result = input_data.to_dict(orient="records")

    return jsonify(result)

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
