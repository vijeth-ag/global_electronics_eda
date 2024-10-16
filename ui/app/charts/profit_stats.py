import streamlit as st
import pandas as pd

from queries import profit_margin


def display_profit_stats():
    
    results = profit_margin()

    st.write("Most profitable products")

    most_profitable_df = pd.DataFrame(results["most_profitable"], columns=["Product Name", "Cost", "Price", "Profit %"])
    st.write(most_profitable_df)
    
    st.write("____________________________________________________________________")

    st.write("Least profitable products")

    least_profitable_df = pd.DataFrame(results["least_profitable"], columns=["Product Name", "Cost", "Price", "Profit %"])
    st.write(least_profitable_df)
