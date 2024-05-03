import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 



def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    
    df = df[df["ConvertedCompYearly"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["ConvertedCompYearly"] <= 350000]
    df = df[df["ConvertedCompYearly"] >= 10000]
    df = df[df['Country'] != 'Other']

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)

    return df

df = load_data()


def show_explore_page():

    st.title("Explore Software Engineer Salaries")
    st.write("""### Stack Overflow Developer Survey 2023""")

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots(figsize=(8, 5))  # Adjusted size for better visualization
    # Draw the pie chart with percentages outside the slices
    wedges, _, autotexts = ax1.pie(data, autopct="%1.0f%%", pctdistance=1.2, shadow=True, startangle=90)
    ax1.axis("equal")  # Ensures that pie is drawn as a circle.

    # Adjust the text properties to improve readability
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)
        autotext.set_horizontalalignment('center')

    # Adding a legend outside the pie chart
    ax1.legend(wedges, data.index, title="Countries", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    st.write("""#### Number of Data from different countries""")
    st.pyplot(fig1)
    st.write( """#### Mean Salary Based On Country""")
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
