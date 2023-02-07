import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'other'
    return categorical_map


def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5

    return float(x)

def clean_education(x):
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than Bachelors'

@st.cache   # avoid loading this again and again
def load_data():
    #all the codes from notebook
    df = pd.read_csv('datasets/survey_results_public.csv')

    df = df[['Country', 'EdLevel', 'YearsCode', 'Employment', 'ConvertedCompYearly']]

    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)

    df.dropna(inplace=True)

    df = df[df['Employment'] == 'Employed, full-time']
    df = df.drop('Employment', axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 300)
    df['Country'] = df['Country'].map(country_map)

    df = df[df['Salary'] <= 150000]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != 'Other']

    df['YearsCode'] = df['YearsCode'].apply(clean_experience)

    df['EdLevel'] = df['EdLevel'].apply(clean_education)

    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Developer Salary")

    st.write("""### Stack Overflow Developer Servey 2022 """)
    data = df['Country'].value_counts()

# Pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels = data.index, autopct = '%1.1f%%', startangle = 90)
    ax1.axis('equal')

    st.write(""" #### Number of Data from different countries """)
    st.pyplot(fig1)

# Bar chart
    st.write("""#### Mean salary based on country """)

    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending = True)
    st.bar_chart(data)

# Line chart
    st.write("""#### Mean salary based on experience """)
    data = df.groupby(['YearsCode'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)