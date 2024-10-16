import streamlit as st

from charts import month_wise_sales, in_demand_product, top_customers, delivery_time, profit_stats, store_stats, custom_query


st.sidebar.title("Analysis")

def show_month_wise_sales():
    month_wise_sales.display_monthly_sales()

def show_in_demand_product():    
    in_demand_product.display_top_selling_products()
    in_demand_product.display_least_selling_products()

def top_10_customers():
    st.write("Top 20 customers")
    top_customers.display_top_customers()

def avg_delivery_time():
    delivery_time.display_avg_delivery_time()

def profit_margin():
    profit_stats.display_profit_stats()

def store_details():
    store_stats.display_store_details()

def custom_llm_query():
    custom_query.display_custome_query_form()


    

# Add buttons to the sidebar and store the selected option in a variable
selected_option = st.sidebar.radio("Select an Option", ("Store Details","Profit Margin", "Delivery time","Top 20 customers","Month wise sales", "Top & Least selling products", "Customer Query"))

# Create a mapping of options to functions
option_map = {
    "Store Details": store_details,
    "Profit Margin": profit_margin,
    "Delivery time": avg_delivery_time,
    "Top 20 customers": top_10_customers,
    "Month wise sales": show_month_wise_sales,
    "Top & Least selling products": show_in_demand_product,
    "Customer Query": custom_llm_query
}

option_map[selected_option]()

