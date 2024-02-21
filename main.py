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


st.title('Food Recommendation System')
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)


selected_diseases = st.sidebar.multiselect('Select Disease(s):', ['Hypertension', 'Diabetes(Type-1)', 'Skin Cancer', 'general'], default=['general'])


top_n_recommend = st.sidebar.slider('Number of Recommended Foods', min_value=1, max_value=20, value=10)
top_n_avoid = st.sidebar.slider('Number of Foods to Avoid', min_value=1, max_value=20, value=10)


st.sidebar.subheader('Selected Diseases:')
for disease in selected_diseases:
    st.sidebar.write("- " + disease)


if st.sidebar.button('Recommend'):
    
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


st.sidebar.markdown("---")
st.sidebar.subheader("")
st.sidebar.markdown("""

""")
