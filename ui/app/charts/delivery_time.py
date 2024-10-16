import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


from queries import get_avg_delivery_times

def display_avg_delivery_time():
    delivery_times = get_avg_delivery_times()

    st.write("Average Delivery Time in Days", delivery_times["avg_del_time"], "days")

    st.write("__________________________________________________________________________________________")
    st.write("Fastest Deliveries")

    fastest_deliveries_df = pd.DataFrame(delivery_times["fastest_deliveries"], columns=["ProductKey", "Product Name", "Delivery Time in days"])
    fastest_deliveries_df = fastest_deliveries_df.drop(["ProductKey"], axis=1)
    st.write(fastest_deliveries_df)
    

    st.write("__________________________________________________________________________________________")
    st.write("Slowest Deliveries")

    slowest_deliveries_df = pd.DataFrame(delivery_times["slowest_deliveries"], columns=["ProductKey", "Product Name", "Delivery Time in days"])
    slowest_deliveries_df = slowest_deliveries_df.drop(["ProductKey"], axis=1)
    st.write(slowest_deliveries_df)



