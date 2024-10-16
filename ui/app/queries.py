import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
from openai import OpenAI


client = OpenAI(
    # This is the default and can be omitted
    api_key="sk-",
)



# Function to create a MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',        # e.g., 'localhost' or your remote host
            user='user',        # your MySQL username
            password='password',  # your MySQL password
            database='my_database'  # name of the database
        )
        if connection.is_connected():            
            return connection
    except Error as e:
        print("Error creating conenction",e)
        return None

create_connection()

# Function to fetch monthly sales for a given year
def get_monthly_sales(year):
    connection = create_connection()
    if connection:
        try:
            query = f"""
                SELECT 
                    `Order Date`, 
                    Quantity
                FROM 
                    sales
                WHERE 
                    YEAR(STR_TO_DATE(`Order Date`, '%m/%d/%Y')) = {year};
            """
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            # Create a DataFrame from the query result
            data = pd.DataFrame(result, columns=['OrderDate', 'Quantity'])
            
            # Convert OrderDate column to a proper date format
            data['OrderDate'] = pd.to_datetime(data['OrderDate'], format='%m/%d/%Y')

            # Extract month and aggregate sales by month
            data['Month'] = data['OrderDate'].dt.month
            monthly_sales = data.groupby('Month')['Quantity'].sum().reset_index()

            return monthly_sales
        except Error as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()
            connection.close()
    return None


def get_top_selling_products():
    connection = create_connection()
    if connection:
        try:
            query = """
                SELECT products.ProductKey, products.`Product Name`, SUM(sales.Quantity) AS Total_Quantity
                FROM products
                JOIN sales ON products.ProductKey = sales.ProductKey
                GROUP BY products.ProductKey, products.`Product Name` ORDER BY `Total_Quantity` desc LIMIT 10 
            """
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            # Create a DataFrame from the query result
            data = pd.DataFrame(result, columns=['Product Key', 'Product Name', 'Total_Quantity'])
            return data
        finally:
            cursor.close()
            connection.close()
    return None    

def get_least_selling_products():
    connection = create_connection()
    if connection:
        try:
            query = """
                SELECT products.ProductKey, products.`Product Name`, SUM(sales.Quantity) AS Total_Quantity
                FROM products
                JOIN sales ON products.ProductKey = sales.ProductKey
                GROUP BY products.ProductKey, products.`Product Name` ORDER BY `Total_Quantity` asc LIMIT 10 
            """
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            # Create a DataFrame from the query result
            data = pd.DataFrame(result, columns=['Product Key', 'Product Name', 'Total_Quantity'])
            return data
        finally:
            cursor.close()
            connection.close()
    return None


def get_top_customers():
    connection = create_connection()
    if connection:
        try:
            query = """
                SELECT customer.`CustomerKey`, customer.`Gender`, customer.`City`, customer.`Country`,customer.age, SUM(sales.Quantity) AS Total_Quantity
                FROM customer
                JOIN sales ON customer.`CustomerKey` = sales.`CustomerKey`
                GROUP BY customer.`CustomerKey`,customer.`Gender`, customer.`City`, customer.`Country`,customer.age ORDER BY `Total_Quantity` desc LIMIT 20               
            """
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            connection.close()
    return None


def get_avg_delivery_times():
    connection = create_connection()
    results = {}
    if connection:
        try:
            query_avg_delivery_time = """
                SELECT AVG(DATEDIFF(STR_TO_DATE(`Delivery Date`, '%m/%d/%Y'), STR_TO_DATE(`Order Date`, '%m/%d/%Y'))) AS avg_delivery_time_in_days
                FROM sales
                WHERE `Order Date` IS NOT NULL AND `Delivery Date` IS NOT NULL                
            """
            cursor = connection.cursor()
            cursor.execute(query_avg_delivery_time)
            result = cursor.fetchall()
            results["avg_del_time"] = result[0][0]

            query_slowest_deliveries = """
                SELECT 
                    s.ProductKey, 
                    p.`Product Name`, 
                    DATEDIFF(STR_TO_DATE(s.`Delivery Date`, '%m/%d/%Y'), STR_TO_DATE(s.`Order Date`, '%m/%d/%Y')) AS avg_delivery_time_in_days
                FROM 
                    sales s
                JOIN 
                    products p ON s.ProductKey = p.ProductKey
                WHERE 
                    s.`Order Date` IS NOT NULL AND s.`Delivery Date` IS NOT NULL 
                ORDER BY 
                    avg_delivery_time_in_days DESC 
                LIMIT 100;
            """
            cursor = connection.cursor()
            cursor.execute(query_slowest_deliveries)
            slowest_deliveries_result = cursor.fetchall()
            results["slowest_deliveries"] = slowest_deliveries_result



            query_fastest_deliveries = """
                SELECT 
                    s.ProductKey, 
                    p.`Product Name`, 
                    DATEDIFF(STR_TO_DATE(s.`Delivery Date`, '%m/%d/%Y'), STR_TO_DATE(s.`Order Date`, '%m/%d/%Y')) AS avg_delivery_time_in_days
                FROM 
                    sales s
                JOIN 
                    products p ON s.ProductKey = p.ProductKey
                WHERE 
                    s.`Order Date` IS NOT NULL AND s.`Delivery Date` IS NOT NULL 
                ORDER BY 
                    avg_delivery_time_in_days ASC 
                LIMIT 100;
            """
            cursor = connection.cursor()
            cursor.execute(query_fastest_deliveries)
            fastest_deliveries_result = cursor.fetchall()
            results["fastest_deliveries"] = fastest_deliveries_result


            return results
        finally:
            cursor.close()
            connection.close()
    return None


def profit_margin():
    connection = create_connection()
    results = {}
    if connection:
        try:
            query_most_profit = """
                SELECT * FROM (
                    SELECT 
                        products.`Product Name`, 
                        CAST(REPLACE(REPLACE(`Unit Cost USD`, '$', ''), ',', '') AS DECIMAL(10, 4)) AS `Unit Cost USD`, 
                        CAST(REPLACE(REPLACE(`Unit Price USD`, '$', ''), ',', '') AS DECIMAL(10, 4)) AS `Unit Price USD`, 
                        ((CAST(REPLACE(REPLACE(`Unit Price USD`, '$', ''), ',', '') AS DECIMAL(10, 2)) - 
                        CAST(REPLACE(REPLACE(`Unit Cost USD`, '$', ''), ',', '') AS DECIMAL(10, 2))) /
                        CAST(REPLACE(REPLACE(`Unit Cost USD`, '$', ''), ',', '') AS DECIMAL(10, 2)) * 100) AS profit_loss_percentage
                    FROM 
                        products
                ) AS product_margins
                ORDER BY profit_loss_percentage DESC
                LIMIT 20;
            """
            cursor = connection.cursor()
            cursor.execute(query_most_profit)
            result = cursor.fetchall()
            results["most_profitable"] = result
            
            
            query_least_profit = """
                SELECT * FROM (
                    SELECT 
                        products.`Product Name`, 
                        CAST(REPLACE(REPLACE(`Unit Cost USD`, '$', ''), ',', '') AS DECIMAL(10, 4)) AS `Unit Cost USD`, 
                        CAST(REPLACE(REPLACE(`Unit Price USD`, '$', ''), ',', '') AS DECIMAL(10, 4)) AS `Unit Price USD`, 
                        ((CAST(REPLACE(REPLACE(`Unit Price USD`, '$', ''), ',', '') AS DECIMAL(10, 2)) - 
                        CAST(REPLACE(REPLACE(`Unit Cost USD`, '$', ''), ',', '') AS DECIMAL(10, 2))) /
                        CAST(REPLACE(REPLACE(`Unit Cost USD`, '$', ''), ',', '') AS DECIMAL(10, 2)) * 100) AS profit_loss_percentage
                    FROM 
                        products
                ) AS product_margins
                ORDER BY profit_loss_percentage ASC
                LIMIT 20;
            """
            cursor = connection.cursor()
            cursor.execute(query_least_profit)
            result = cursor.fetchall()
            results["least_profitable"] = result            
            
            
            
            return results
        finally:
            cursor.close()
            connection.close()
    return None

def store_details():
    connection = create_connection()
    results = {}

    query_total_sales_quantity_store = """
        SELECT 
            s.StoreKey, 
            s.Country, 
            s.State, 
            s.`Square Meters`, 
            s.`Open Date`, 
            SUM(sa.Quantity) AS Total_Quantity
        FROM 
            sales sa
        JOIN 
            stores s ON sa.StoreKey = s.StoreKey
        GROUP BY 
            s.StoreKey, s.Country, s.State, s.`Square Meters`, s.`Open Date`
        ORDER BY 
            Total_Quantity DESC;
    """

    cursor = connection.cursor()
    cursor.execute(query_total_sales_quantity_store)
    result = cursor.fetchall()
    results["total_sales_quantity_store"] = result


    query_count_unique_customers_per_store = """
        SELECT 
            s.StoreKey, 
            s.Country, 
            s.State, 
            s.`Square Meters`, 
            s.`Open Date`, 
            COUNT(DISTINCT sa.CustomerKey) AS Unique_Customers
        FROM 
            sales sa
        JOIN 
            stores s ON sa.StoreKey = s.StoreKey
        GROUP BY 
            s.StoreKey, s.Country, s.State, s.`Square Meters`, s.`Open Date`
        ORDER BY 
            Unique_Customers DESC;
    """

    cursor = connection.cursor()
    cursor.execute(query_count_unique_customers_per_store)
    result = cursor.fetchall()
    results["count_unique_customers_per_store"] = result

    query_average_quantity_sold_per_store = """
        SELECT 
            s.StoreKey, 
            s.Country, 
            s.State, 
            s.`Square Meters`, 
            s.`Open Date`, 
            AVG(sa.Quantity) AS Average_Quantity_Sold
        FROM 
            sales sa
        JOIN 
            stores s ON sa.StoreKey = s.StoreKey
        GROUP BY 
            s.StoreKey, s.Country, s.State, s.`Square Meters`, s.`Open Date`
        ORDER BY 
            Average_Quantity_Sold DESC
        LIMIT 10;
    """

    cursor = connection.cursor()
    cursor.execute(query_average_quantity_sold_per_store)
    result = cursor.fetchall()
    results["average_quantity_sold_per_store"] = result

    return results


def get_sql_command(english_text):
    # System prompt to provide context
    system_prompt = (
        "You are an SQL expert. You just reply the sql command as basic string. You have access to the following database schema:\n"
        "Tables:\n"
        "1. customer (CustomerKey, Gender, Name, City, State Code, State, ZipCode, Country, COntinent, age)\n"
        "2. sales (Order Number, Line Item, Order Date, Delivery Date,CustomerKey, StoreKey,ProductKey, Quantity, Currency Code)\n"
        "3. products (ProductKey, Product Name, Brand, Color, `Unit Cost USD`, `Unit Price USD`, SubcategoryKey, CategoryKey, Category)\n"
        "4. stores (StoreKey, Country, State, `Square Meters`, `Open Date`)\n"
        "Please convert the following English text into a corresponding SQL command."
    )

    # Combine system prompt and user input
    prompt = f"{system_prompt}\n\nEnglish text: '{english_text}'"
    
    try:
        # Make a request to the OpenAI API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role":"system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )

        print("chat_completion",chat_completion.choices[0].message.content)
        
        # Extract the SQL command from the response
        sql_command = chat_completion.choices[0].message.content
        return sql_command
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_result_for_custom_query(txt_query):
    sql_cmd = get_sql_command(txt_query)
    print("generated sql command", sql_cmd)

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(sql_cmd)
    result = cursor.fetchall()
    return result
