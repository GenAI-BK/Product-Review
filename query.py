import sqlite3
import pandas as pd
DATABASE_PATH = 'supply_database.db'

def show_data(product_name):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    query = '''
    SELECT * FROM reviews
    WHERE product_name = ?
    '''

    # Execute the query
    
    cursor.execute(query, (product_name,))

    # Fetch all rows
    df = pd.read_sql_query(query, conn, params=(product_name,))
    conn.close()
    if df.shape[0]>=300:
        df=df[:250]
    return df
   
    
def query_data(product_name):
    # Define the SQL query
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    query = '''
    SELECT * FROM reviews
    WHERE product_name = ?
    '''

    # Execute the query
    
    cursor.execute(query, (product_name,))

    # Fetch all rows
    data = cursor.fetchall()
    
        
    # Close the connection
    conn.close()
    if len(data)>=300:
        data=data[:250]

    return data
def lst_product():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Define the SQL query to fetch unique product names
    query = 'SELECT DISTINCT product_name FROM reviews'

    # Execute the query
    cursor.execute(query)

    # Fetch all unique product names
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Extract the product names from the rows and return as a list
    product_names = [row[0] for row in rows]
    return product_names
lst=show_data('BoAt_Rockerz_235v2_with_ASAP_charging_Version_5.0_Bluetooth_Headset')
# # print(lst_product())
# print(lst)
    
        
