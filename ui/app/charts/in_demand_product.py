import streamlit as st
import matplotlib.pyplot as plt

from queries import get_top_selling_products, get_least_selling_products


def display_top_selling_products():
    st.write("Top Selling Products")
    
    top_products = get_top_selling_products()
    low_selling_products = get_least_selling_products()

    print("low_selling_products",low_selling_products)

    if top_products is not None and not top_products.empty:
        # Plotting
        fig, ax = plt.subplots(figsize=(8, 5))  # Adjust figure size as needed
        ax.bar(top_products['Product Name'], top_products['Total_Quantity'], color='skyblue')
        ax.set_xlabel('Product Name')
        ax.set_ylabel('Total Sales (Quantity)')
        ax.set_title('Top 10 Selling Products')
        ax.set_xticklabels(top_products['Product Name'], rotation=45, ha='right')

        # Display the plot in Streamlit
        st.pyplot(fig)
    else:
        st.write("No data available.")   

def display_least_selling_products():
    st.write("Least Selling Products")
    
    top_products = get_top_selling_products()
    low_selling_products = get_least_selling_products()

    print("low_selling_products",low_selling_products)

    if low_selling_products is not None and not low_selling_products.empty:
        # Plotting
        fig, ax = plt.subplots(figsize=(8, 5))  # Adjust figure size as needed
        ax.bar(low_selling_products['Product Name'], low_selling_products['Total_Quantity'], color='blue')
        ax.set_xlabel('Product Name')
        ax.set_ylabel('Total Sales (Quantity)')
        ax.set_title('Least 10 Selling Products')
        ax.set_xticklabels(low_selling_products['Product Name'], rotation=45, ha='right')

        # Display the plot in Streamlit
        st.pyplot(fig)
    else:
        st.write("No data available.")            