# import numpy as np
import pandas as pd
import pickle

# Read the preprocessed data
food_df = pd.read_csv('model/datasets/preprocessed_food.csv')
disease_df = pd.read_csv('model/datasets/preprocessed_recommendedfordisease.csv')

# Define the list of diseases
diseases = ["AcidReflux", "Anemia", "Cavities", "FattyLiver", "Gastritis",
            "Obesity", "Pancreatitis", "Type1Diabetes", "Urinary-tract",
            "Hypertension", "Low Blood Pressure", "Kidney Stone",
            "coronary artery disease", "bronchitis", "asthma",
            "common cold", "influenza", "corona virus", "diarrhoea", "cholera"]

# Dictionary with disease names as keys and indices values
disease_dict = {disease: i for i, disease in enumerate(diseases)}

# Prompt the user to choose a disease index
choice = input("Enter the disease index (0 to 19): ")
if choice.isdigit() and int(choice) in range(20):
    disease_index = int(choice)
    selected_disease = diseases[disease_index]

    # Load the model from the pickle file
    pickle_filename = f'model/saved_models/recommended_food_{disease_index}.pkl'
    with open(pickle_filename, 'rb') as pickle_file:
        loaded_model_foodidx = pickle.load(pickle_file)

    # Print the top recommended foods
    print("\nTop Recommended Foods for", selected_disease)
    unique_first_words = set()
    unique_second_words = set()
    for i, idx in enumerate(loaded_model_foodidx):
        food_name = food_df.loc[idx, 'Name']
        if len(food_name.split()) >= 2:
            first_word, second_word, *_ = food_name.split()
            if first_word not in unique_first_words and second_word not in unique_second_words:
                print(f"{i+1}. {food_name}")
                unique_first_words.add(first_word)
                unique_second_words.add(second_word)
        else:
            print(f"{i+1}. {food_name}")
else:
    print("Invalid choice. Please enter a number between 0 and 19.")