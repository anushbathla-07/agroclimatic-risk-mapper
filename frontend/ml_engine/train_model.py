import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

print("🌱 Initializing ML Training Sequence...")

# ---------------------------------------------------------
# 1. GENERATE SYNTHETIC DATASET
# ---------------------------------------------------------
# We are creating 5,000 rows of dummy data for our model to learn from.
np.random.seed(42)
num_samples = 5000

# Randomly assign crops
crops = np.random.choice(['Sugarcane', 'Wheat', 'Rice'], num_samples)

# Generate random weather conditions
max_temps = np.random.uniform(20.0, 45.0, num_samples)
min_temps = np.random.uniform(5.0, 30.0, num_samples)
rainfall = np.random.uniform(0.0, 2000.0, num_samples)

# Create a DataFrame
df = pd.DataFrame({
    'crop': crops,
    'temperature_max': max_temps,
    'temperature_min': min_temps,
    'rainfall_mm': rainfall
})

# Define the "Ground Truth" Logic for the AI to learn
def calculate_historical_risk(row):
    risk_score = 0
    if row['crop'] == 'Sugarcane':
        if row['temperature_max'] > 38 or row['temperature_min'] < 10: risk_score += 4
        if row['rainfall_mm'] < 1000: risk_score += 5
    elif row['crop'] == 'Wheat':
        if row['temperature_max'] > 30 or row['temperature_min'] < 5: risk_score += 4
        if row['rainfall_mm'] < 300: risk_score += 5
    elif row['crop'] == 'Rice':
        if row['temperature_max'] > 40 or row['temperature_min'] < 15: risk_score += 4
        if row['rainfall_mm'] < 1200: risk_score += 5
        
    if risk_score >= 5: return "High"
    elif risk_score >= 4: return "Moderate"
    else: return "Low"

# Apply the logic to create our target variable (what the AI needs to predict)
df['risk_level'] = df.apply(calculate_historical_risk, axis=1)

print(f"📊 Synthetic dataset generated with {num_samples} records.")

# ---------------------------------------------------------
# 2. PRE-PROCESS DATA FOR MACHINE LEARNING
# ---------------------------------------------------------
# AI models only understand numbers, so we must encode the text (crop names) into numbers
label_encoder = LabelEncoder()
df['crop_encoded'] = label_encoder.fit_transform(df['crop'])

# Define X (Features/Inputs) and y (Target/Output)
X = df[['crop_encoded', 'temperature_max', 'temperature_min', 'rainfall_mm']]
y = df['risk_level']

# Split data into 80% training and 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------------------------------------------
# 3. TRAIN THE RANDOM FOREST MODEL
# ---------------------------------------------------------
print("🧠 Training Random Forest Classifier...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Check accuracy
accuracy = model.score(X_test, y_test)
print(f"🎯 Model Accuracy on Test Data: {accuracy * 100:.2f}%")

# ---------------------------------------------------------
# 4. EXPORT THE TRAINED MODEL (The "Brain")
# ---------------------------------------------------------
# Ensure the directory exists
os.makedirs('saved_models', exist_ok=True)

# Save both the model and the encoder (so we can translate text inputs later)
joblib.dump(model, 'saved_models/random_forest_risk_model.pkl')
joblib.dump(label_encoder, 'saved_models/crop_label_encoder.pkl')

print("✅ Model and Encoder successfully saved in 'saved_models/' folder!")