import streamlit as st
import calendar
import matplotlib.pyplot as plt

from queries import get_monthly_sales


def display_monthly_sales():
    st.write("Monthly Sales for a Given Year")

    # Input field to accept a year from the user
    year = st.number_input("Enter the year", min_value=2000, max_value=2100, value=2016, step=1)

    # Fetch data when button is clicked
    if st.button("Fetch Monthly Sales"):
        monthly_sales = get_monthly_sales(year)
        
        if monthly_sales is not None and not monthly_sales.empty:
            month_names = [calendar.month_abbr[month] for month in monthly_sales['Month']]

            # Plotting the bar chart
            fig, ax = plt.subplots(figsize=(3, 2))
            ax.bar(monthly_sales['Month'], monthly_sales['Quantity'], color='skyblue', width=0.6)
            ax.set_xlabel('Month')
            ax.set_ylabel('Total Sales (Quantity)', fontsize=5)
            ax.set_title(f'Monthly Sales for {year}', fontsize=5)
            ax.set_xticks(monthly_sales['Month'])
            ax.set_xticklabels(month_names, rotation=45)
            
            # Display the plot in Streamlit
            st.pyplot(fig)
        else:
            st.warning(f"No sales data found for the year {year}")
            
display_monthly_sales()    