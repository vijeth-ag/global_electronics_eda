import streamlit as st
import pandas as pd

from queries import get_result_for_custom_query


def display_custome_query_form():
    st.write("Custom Query")

    # Streamlit form
    with st.form(key='my_form'):
        # Input fields
        text_query = st.text_input("Enter your query:")

        # Submit button
        submit_button = st.form_submit_button(label='Submit')

    # Action on submit
    if submit_button:
        result = get_result_for_custom_query(text_query)
        res_df = pd.DataFrame()
        for row in result:
            res_df = res_df.append(pd.DataFrame([row]))
        st.write(res_df)