import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
food_data = pd.read_csv('preprocessed_food.csv')
disease_data = pd.read_csv('preprocessed_disease.csv')
selected_disease = input("Enter the disease name: ")

disease_limits = disease_data[disease_data['disease_name'] == selected_disease].iloc[:, 1:].values

nutrient_columns = food_data.columns[1:]
food_nutrition = food_data[nutrient_columns].values

distance = disease_limits - food_nutrition

distance_magnitude = np.linalg.norm(distance, axis=1)

food_distance_df = pd.DataFrame({'Food': food_data['name'], 'Distance': distance_magnitude})

X = food_nutrition
y = distance_magnitude
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
predicted_distances = model.predict(food_nutrition)
top_n = 30
recommended_food_indices = np.argsort(predicted_distances)[:top_n]

print("Top Recommended Foods for", selected_disease)
for i, idx in enumerate(recommended_food_indices):
    food_name = food_data.loc[idx, 'name']
    print(f"{i+1}. {food_name}")