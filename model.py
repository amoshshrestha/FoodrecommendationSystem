import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# Load data
food_data = pd.read_csv('preprocessed_food.csv')
disease_data = pd.read_csv('preprocessed_disease.csv')

# Get user input
selected_disease = input("Enter the disease name: ")

# Extract disease limits
disease_limits = disease_data[disease_data['disease_name'] == selected_disease].iloc[:, 1:].values

# Extract nutrient columns and create features
nutrient_columns = food_data.columns[1:]
food_nutrition = food_data[nutrient_columns].values

# Feature engineering (example: nutrient ratios)
food_nutrition = np.hstack((food_nutrition, food_nutrition[:, 1] / food_nutrition[:, 2]))  # Add fat-to-protein ratio

# Normalize data
scaler = StandardScaler()
food_nutrition_scaled = scaler.fit_transform(food_nutrition)
disease_limits_scaled = scaler.transform(disease_limits)

# Split data
X_train, X_test, y_train, y_test = train_test_split(food_nutrition_scaled, disease_limits_scaled, test_size=0.2, random_state=42)

# KNN model
knn = KNeighborsRegressor(n_neighbors=5)  # Adjust hyperparameters as needed
knn.fit(X_train, y_train)

# Predict distances
predicted_distances = knn.predict(food_nutrition_scaled)

# Find recommended and avoid foods
recommended_food_indices = np.argsort(predicted_distances)[:30]  # Top 30 recommendations
avoid_food_indices = np.argsort(-predicted_distances)[:30]  # Top 30 to avoid

# Display recommendations and foods to avoid
print("\nRecommended Foods for", selected_disease)
for i, idx in enumerate(recommended_food_indices):
    food_name = food_data.loc[idx, 'name']
    print(f"{i+1}. {food_name}")

print("\nFoods to Avoid for", selected_disease)
for i, idx in enumerate(avoid_food_indices):
    food_name = food_data.loc[idx, 'name']
    print(f"{i+1}. {food_name}")
