import streamlit as st
import pickle 
import numpy as np 

similarity_scores = pickle.load(open('model/similarity_scores.pkl','rb'))
food_data = pickle.load(open('model/food.pkl','rb'))
disease_data = pickle.load(open('model/disease.pkl','rb'))

st.title('Food Recommendation System')

disease= st.selectbox('Select Disease: ', ['Hypertension', 
                                         'Diabetes(Type-1)', 
                                         'Skin Cancer', 
                                         'general'])

if st.button('Recommend'):
    similarity_scores_selected_disease = similarity_scores[disease]

    # Create two column layout
    left_column, right_column = st.columns(2)

    with left_column:
        # Get Top Recommended foods
        top_food_indices = np.argsort(similarity_scores_selected_disease)[:5]
        recommended_foods = food_data.loc[top_food_indices, 'name'].tolist()

        # Display recommended foods
        st.subheader('Top Recommended Foods')
        for i, food in enumerate(recommended_foods, start=1):
            st.write(f"{i}. {food}")
            
    with right_column:
        # Avoid foods
        avoid_food_indices = np.argsort(similarity_scores_selected_disease)[-5:][::-1]
        not_recommended_foods = food_data.loc[avoid_food_indices, 'name'].tolist()

        # Display not recommended foods
        st.subheader('Avoid Foods')
        for i, food in enumerate(not_recommended_foods, start=1):
            st.write(f"{i}. {food}")
