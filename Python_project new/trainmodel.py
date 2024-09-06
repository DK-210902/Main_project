import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Load the dataset
df = pd.read_csv('delivery_data.csv')

# Define features and target variable
X = df[['Source lat', 'source lon', 'destn lat', 'destn lon', 'payload']]
y = df['money']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'model.pkl')

print("Model trained and saved as 'model.pkl'")
a = {
    'Source lat': [59.3851719],  
    'source lon': [17.9172006],  
    'destn lat': [14.43201],    
    'destn lon': [46.15435],  
    'payload':[3990]          
}


input_df = pd.DataFrame(a)
# Predict using the hardcoded input
predicted_money = model.predict(input_df)[0]
rounded_money = round(predicted_money, 2)  # Rounded to 2 decimal places
print(f"Predicted money for the hardcoded input: ${rounded_money:.2f}")