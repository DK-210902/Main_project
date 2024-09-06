from flask import Flask, request, render_template
import joblib
import pandas as pd
import numpy as np
from truck import Truck

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = joblib.load('model.pkl')

# Initialize trucks
trucks = [
    Truck(0, 0, 15000, 'Mahindra', 15),
    Truck(5, 10, 10000, 'Tata', 20),
    Truck(3, 7, 12000, 'Ashok Leyland', 17)
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve and convert input values
        source_lat = float(request.form.get('source_lat'))
        source_lon = float(request.form.get('source_lon'))
        destn_lat = float(request.form.get('destn_lat'))
        destn_lon = float(request.form.get('destn_lon'))
        payload = float(request.form.get('payload'))
    except (ValueError, TypeError):
        return "Invalid input. Please enter numeric values.", 400

    # Create a DataFrame from the input values
    input_df = pd.DataFrame({
        'Source lat': [source_lat],
        'Source lon': [source_lon],
        'destn lat': [destn_lat],
        'destn lon': [destn_lon],
        'payload': [payload]
    })

    # Define the expected feature columns
    expected_features = ['Source lat', 'Source lon', 'destn lat', 'destn lon', 'payload']

    # Ensure the DataFrame has the correct columns
    if set(expected_features) != set(input_df.columns):
        return "Input DataFrame does not have the correct feature columns.", 400

    # Check for correct number of features
    if input_df.shape[1] != len(expected_features):
        return "Input DataFrame has an incorrect number of features.", 400

    try:
        # Extract the features in the correct order
        input_data = input_df[expected_features].values
        predicted_money = model.predict(input_data)[0]
        rounded_money = round(predicted_money, 2) 

    except Exception as e:
        return f"Error making prediction: {e}. Please try again later.", 500

    # Find the best truck for delivery
    min_cost = float('inf')
    best_truck = None

    for truck in trucks:
        can_handle, distance, cost = truck.can_handle_delivery(destn_lat, destn_lon, payload)
        if can_handle and cost < min_cost:
            min_cost = cost
            best_truck = truck

    if best_truck:
        truck_info = f"Best truck for delivery at ({destn_lat}, {destn_lon}) is {best_truck.name} ."
    else:
        truck_info = "No trucks can handle the delivery with the specified payload."

    return render_template('result.html', prediction=rounded_money, truck_info=truck_info)

if __name__ == '__main__':
    app.run(debug=True)