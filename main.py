from flask import Flask, render_template, request, url_for
from algoliasearch.search_client import SearchClient
import requests
# from math import ceil
import os
import pandas as pd
import pickle
from dotenv import load_dotenv
load_dotenv()

# Access environment variables
ALGOLIA_INDEX_NAME= os.getenv("ALGOLIA_INDEX_NAME")
ALGOLIA_API_KEY= os.getenv("ALGOLIA_API_KEY")
ALGOLIA_APP_ID = os.getenv("ALGOLIA_APP_ID")

app = Flask(__name__)

# Static location config
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = 'static'
app.secret_key = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = 'static'

# Load preprocessed data
food_df = pd.read_csv('model/datasets/preprocessed_food.csv')

# Define list of diseases
diseases = ["AcidReflux", "Anemia", "Cavities", "FattyLiver", "Gastritis",
            "Obesity", "Pancreatitis", "Type1Diabetes", "Urinary-tract",
            "Hypertension", "Low Blood Pressure", "Kidney Stone",
            "coronary artery disease", "bronchitis", "asthma",
            "common cold", "influenza", "corona virus", "diarrhoea", "cholera"]

# Dictionary with disease names as keys and indices values
disease_dict = {disease: i for i, disease in enumerate(diseases)}

""" Setting Template """
@app.route('/')
def home():
    return render_template('home.html' )


@app.route('/recommend', methods=['POST','GET'])
def recommend():
    if request.method == 'GET':
        return render_template('food_recommend.html', diseases=diseases)
    elif request.method == 'POST':
        selected_disease = request.form.get('disease')
        print("Form Data:", request.form)  # Print form data for debugging
        print("Selected Disease:", selected_disease)  # Print selected disease
        disease_index = disease_dict.get(selected_disease)
        if disease_index is None:
            return "Invalid disease selected."  # Handle case where disease is not found

        # Load the model from the pickle file
        pickle_filename = f'model/saved_models/recommended_food_{disease_index}.pkl'
        with open(pickle_filename, 'rb') as pickle_file:
            loaded_model_foodidx = pickle.load(pickle_file)

        # Get top recommended foods
        recommended_foods = []
        unique_first_words = set()
        unique_second_words = set()
        for idx in loaded_model_foodidx:
            food_name = food_df.loc[idx, 'Name']
            if len(food_name.split()) >= 2:
                first_word, second_word, *_ = food_name.split()
                if first_word not in unique_first_words and second_word not in unique_second_words:
                    recommended_foods.append(food_name)
                    unique_first_words.add(first_word)
                    unique_second_words.add(second_word)
            else:
                recommended_foods.append(food_name)

        return render_template('recommendation.html', diseases=diseases,
                                                 selected_disease=selected_disease, 
                                                 recommended_foods=recommended_foods)



@app.route('/foodavoid', methods=['POST','GET'])
def avoid():
    if request.method == 'GET':
        return render_template('food_avoid.html', diseases=diseases)
    elif request.method == 'POST':
        selected_disease = request.form.get('disease')
        print("Form Data:", request.form)  # Print form data for debugging
        print("Selected Disease:", selected_disease)  # Print selected disease
        disease_index = disease_dict.get(selected_disease)
        if disease_index is None:
            return "Invalid disease selected."  # Handle case where disease is not found

        # Load the model from the pickle file
        pickle_filename = f'model/saved_models/avoid_food_{disease_index}.pkl'
        with open(pickle_filename, 'rb') as pickle_file:
            loaded_model_foodidx = pickle.load(pickle_file)

        # Get top avoid foods
        avoid_foods = []
        unique_first_words = set()
        unique_second_words = set()
        for idx in loaded_model_foodidx:
            food_name = food_df.loc[idx, 'Name']
            if len(food_name.split()) >= 2:
                first_word, second_word, *_ = food_name.split()
                if first_word not in unique_first_words and second_word not in unique_second_words:
                    avoid_foods.append(food_name)
                    unique_first_words.add(first_word)
                    unique_second_words.add(second_word)
            else:
                avoid_foods.append(food_name)

        return render_template('avoid.html', diseases=diseases,
                                                    selected_disease=selected_disease, 
                                                    avoid_foods=avoid_foods)

# Algolia Search
client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
index = client.init_index(ALGOLIA_INDEX_NAME)

# Search function
@app.route('/category')
def search():
    query = request.args.get('query')
    format = request.args.get('format', 'html')

    if not query:
        if format == 'json':
            return jsonify({'error': 'query parameter is required'})
        else:
            return render_template('search.html', error='query parameter is required')

    results = index.search(query)
    hits = results['hits']

    if format == 'json':
        return jsonify(hits)
    return render_template('search.html', hits=hits, query=query)

if __name__ == '__main__':
    app.run(debug=True)