import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    countries = (
        'Germany',
        'United Kingdom of Great Britain and Northern Ireland',
        'India',
        'Canada',
        'France',
        'United States of America',
        'Brazil',
        'Spain',
        'Netherlands',
        'Australia',
        'Italy',
        'Poland',
        'Sweden',
        'Russian Federation',
        'Switzerland',
        'Turkey',
        'Israel',
        'Austria'
    )
    education_levels = (
        'Master’s degree',
        'Bachelor’s degree',
        'Less than Bachelors',
        'Post grad'
    )

    country = st.selectbox('Country', countries)
    education = st.selectbox('Education level', education_levels)
    experience = st.slider('Years of Experience',0, 50, 2)

    pred_salary = st.button('Calculate Salary')
    if pred_salary:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f'The estimated salary is ${salary[0]:.2f}')