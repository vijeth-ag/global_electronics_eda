import streamlit as st
import pandas as pd

from queries import store_details

def display_store_details():
    results = store_details()

    st.write("Total Sales Quantity by Store")
    total_sales_quantity_store_df = pd.DataFrame(results["total_sales_quantity_store"], columns=["StoreKey", "Country", "State", "Square Meters", "Date Opened", "Average Quantity Sold"])
    st.write(total_sales_quantity_store_df)

    st.write("______________________________________________________________________")

    st.write("Count Unique Customers per Store")

    count_unique_customers_per_store_df = pd.DataFrame(results["count_unique_customers_per_store"], columns=["StoreKey", "Country", "State", "Square Meters", "Date Opened", "Average Quantity Sold"])
    st.write(count_unique_customers_per_store_df)


    st.write("______________________________________________________________________")
    st.write("Average Quantity Sold per Store")

    average_quantity_sold_per_store_df = pd.DataFrame(results["average_quantity_sold_per_store"], columns=["StoreKey", "Country", "State", "Square Meters", "Date Opened", "Average Quantity Sold"])
    st.write(average_quantity_sold_per_store_df)        