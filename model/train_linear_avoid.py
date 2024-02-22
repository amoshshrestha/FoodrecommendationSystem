import numpy as np
import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# Read the preprocessed data
food_df = pd.read_csv('datasets/preprocessed_food.csv')
disease_df = pd.read_csv('datasets/preprocessed_avoidfordisease.csv')

# Create a dataframe with disease names
disease_df = pd.DataFrame({'Disease': ["AcidReflux", "Anemia", "Cavities", "FattyLiver", "Gastritis",
                                       "Obesity", "Pancreatitis", "Type1Diabetes", "Urinary-tract",
                                       "Hypertension", "Low Blood Pressure", "Kidney Stone",
                                       "coronary artery disease", "bronchitis", "asthma",
                                       "common cold", "influenza", "corona virus", "diarrhoea", "cholera"]})

# Dictionary with disease names as keys and indices values
disease_dict = {disease: i for i, disease in enumerate(disease_df["Disease"])}
# print(disease_dict)

selected_disease = list(disease_dict.keys())

# Create the directory if it doesn't exist
if not os.path.exists('saved_models/'):
    os.makedirs('saved_models/')

# Loop over all selected diseases
for disease in selected_disease:
    disease_df = pd.read_csv('datasets/preprocessed_avoidfordisease.csv')
    # print(disease)

    # Extract disease limits
    disease_limits = disease_df[disease_df['Disease'] == disease].iloc[:, 1:].values
    # print(disease_limits)

    # Extract nutrient columns and food nutrition values
    nutrient_columns = food_df.columns[2:]
    food_nutrition = food_df[nutrient_columns].values
    # print(disease_limits.shape, food_nutrition.shape)
    
    # Calculate distances
    distance = disease_limits - food_nutrition
    distance_magnitude = np.linalg.norm(distance, axis=1)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(food_nutrition,
                                                        distance_magnitude, 
                                                        test_size=0.2, 
                                                        random_state=42)

    # Train linear regression model with polynomial features for complexity
    degree = 3
    model = make_pipeline(PolynomialFeatures(degree), 
                          LinearRegression())

    model.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = model.predict(X_test)

    # Evaluate the model performance
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    # Print the evaluation results
    print(f"\nEvaluation results for {disease}:")
    print("R2 Score:", r2)
    print("MAE:", mae)

    # Predict distances for all foods
    predicted_distances = model.predict(food_nutrition)

    # Save the top 150 avoid food indices in a pickle file
    top_n = 150
    avoid_food_indices = np.argsort(predicted_distances)[:top_n]
    pickle_filename = f'saved_models/avoid_food_{disease_dict[disease]}.pkl'
    with open(pickle_filename, 'wb') as pickle_file:
        pickle.dump(avoid_food_indices, pickle_file)

    print(f'Saved at {pickle_filename} for {disease}')
