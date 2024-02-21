import streamlit as st
import pickle
import numpy as np
import pandas as pd


similarity_scores = pickle.load(open('model/similarity_scores.pkl', 'rb'))
food_data = pickle.load(open('model/food.pkl', 'rb'))
disease_data = pickle.load(open('model/disease.pkl', 'rb'))


custom_css = """
    body {
        color: #262730;
        background-color: #f7f7f7;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #2ecc71;
        color: #ffffff;
        border-radius: 5px;
    }
    .sidebar .sidebar-content {
        background-color: #34495e;
        color: #ffffff;
        border-radius: 5px;
        margin-top: 10px;
    }
    .sidebar .sidebar-content .stButton>button {
        background-color: #3498db;
        border-radius: 5px;
    }
    .stSelectbox {
        background-color: #3498db;
        color: #ffffff;
    }
    .stTable {
        background-color: #ffffff;
    }
    .stTable th, .stTable td {
        border: 1px solid #dddddd;
    }
    .stTable thead th {
        background-color: #2c3e50;
        color: #ffffff;
    }
"""


st.sidebar.title('Food Recommendation System')
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

# Define function to display different pages
def display_food_recommendation():
    st.title("Food Recommendation")
    selected_diseases = st.multiselect('Select Disease(s):', ["AcidReflux","Anemia","Cavities","FattyLiver","Gastritis""Obesity","Pancreatitis","Type1Diabetes","Urinary-tract","Hypertension","Low Blood Pressure","Kidney Stone","coronary artery disease","Bronchitis","Asthma","Common Cold","Influenza","Coronavirus","Diarrhea","Cholera"], default=['AcidReflux'])
    st.subheader('Selected Diseases:')
    for disease in selected_diseases:
        


        if st.button('Recommend'):
            
            for disease in selected_diseases:
                similarity_scores_selected_disease = similarity_scores[disease]

                
                top_food_indices = np.argsort(similarity_scores_selected_disease)[:top_n_recommend]
                recommended_foods = food_data.loc[top_food_indices, 'name'].tolist()

            
                avoid_food_indices = np.argsort(similarity_scores_selected_disease)[-top_n_avoid:][::-1]
                not_recommended_foods = food_data.loc[avoid_food_indices, 'name'].tolist()

            
                col1, col2 = st.columns(2)

                
                with col1:
                    st.subheader(f'Top {top_n_recommend} Recommended Foods for {disease}')
                    for i, food in enumerate(recommended_foods, start=1):
                        intensity = int(((top_n_recommend - i + 1) / top_n_recommend) * 255)  
                        color = f'rgb(0, {255 - intensity*0.8}, 0)'  
                        st.markdown(f"<div style='background-color: {color}; padding: 10px; margin: 5px; border-radius: 5px; color: #ffffff; text-align: center;'>{i}. {food}</div>", unsafe_allow_html=True)

                
                with col2:
                    st.subheader(f'Top {top_n_avoid} Foods to Avoid for {disease}')
                    for i, food in enumerate(not_recommended_foods, start=1):
                        intensity = int(((top_n_avoid - i + 1) / top_n_avoid) * 255)  
                        color = f'rgb(255, {255 - intensity}, {255 - intensity})' 
                        st.markdown(f"<div style='background-color: {color}; padding: 10px; margin: 5px; border-radius: 5px; color: #ffffff; text-align: center;'>{i}. {food}</div>", unsafe_allow_html=True)
        # Add your code for food recommendation here

def display_categorical_food_recommendation():
    st.title("Categorical Food Recommendation")
    # Add your code for categorical food recommendation here

def display_food_to_avoid():
    st.title("Food to Avoid")
    # Add your code for food to avoid here

def display_check_food_for_consumption():
    st.title("Check Food for Consumption")
    # Add your code for checking food for consumption here

# Sidebar (Navbar)
selected_option = st.sidebar.radio("Navigation", ["Food Recommend", "Categorical Food Recommend", "Food to Avoid", "Check Food for Consumption"])

# Main content based on selected option
if selected_option == "Food Recommend":
    display_food_recommendation()

elif selected_option == "Categorical Food Recommend":
    display_categorical_food_recommendation()

elif selected_option == "Food to Avoid":
    display_food_to_avoid()

elif selected_option == "Check Food for Consumption":
    display_check_food_for_consumption()








st.sidebar.markdown("---")
st.sidebar.subheader("")
st.sidebar.markdown("""

""")
