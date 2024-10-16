import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


from queries import get_top_customers

def display_top_customers():
    top_customers = get_top_customers()
    print("top_customers",type(top_customers))
    df = pd.DataFrame(top_customers, columns=['CustomerKey', 'Gender', 'City', 'Country', 'Age', 'Total_Quantity'])
    age_counts = df['Age'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('Age Distribution')
    st.pyplot(fig)

    gender_counts = df['Gender'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('Gender Distribution')
    st.pyplot(fig)

    country_counts = df['Country'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(country_counts, labels=country_counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('Country Distribution')
    st.pyplot(fig)



