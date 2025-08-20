import mysql.connector # type: ignore
import pandas as pd

# --- Connect to MySQL ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harsh@111",  # replace with your password
    database="food_db"         # replace with your database name
)
cursor = conn.cursor()

# --- List of queries ---
queries = {
    "Providers count by city": """
        SELECT City, COUNT(*) AS total_providers 
        FROM providers 
        GROUP BY City;
    """,
    "Top provider types": """
        SELECT Type, COUNT(*) AS total 
        FROM providers 
        GROUP BY Type 
        ORDER BY total DESC;
    """,
    "Provider contact info (Delhi)": """
        SELECT Name, Contact 
        FROM providers 
        WHERE City = 'Delhi';
    """,
    "Receivers count by city": """
        SELECT City, COUNT(*) AS total_receivers 
        FROM receivers 
        GROUP BY City;
    """,
    "Receivers with most claims": """
        SELECT r.Name, COUNT(c.Claim_ID) AS total_claims
        FROM receivers r 
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        GROUP BY r.Name 
        ORDER BY total_claims DESC;
    """,
    "Total food quantity available": """
        SELECT SUM(Quantity) AS total_quantity 
        FROM food_listings;
    """,
    "Cities with highest food listings": """
        SELECT Location, COUNT(*) AS total_listings
        FROM food_listings 
        GROUP BY Location 
        ORDER BY total_listings DESC;
    """,
    "Most common food types": """
        SELECT Food_Type, COUNT(*) AS total_items
        FROM food_listings 
        GROUP BY Food_Type 
        ORDER BY total_items DESC;
    """,
    "Claims count for each food item": """
        SELECT f.Food_Name, COUNT(c.Claim_ID) AS total_claims
        FROM claims c 
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Food_Name;
    """,
    "Provider with highest successful claims": """
        SELECT p.Name, COUNT(c.Claim_ID) AS successful_claims
        FROM providers p
        JOIN food_listings f ON p.Provider_ID = f.Provider_ID
        JOIN claims c ON f.Food_ID = c.Food_ID
        WHERE c.Status = 'Completed'
        GROUP BY p.Name 
        ORDER BY successful_claims DESC;
    """,
    "Claim status distribution": """
        SELECT Status, COUNT(*) AS total_claims
        FROM claims 
        GROUP BY Status;
    """,
    "Average quantity claimed per receiver": """
        SELECT r.Name, AVG(f.Quantity) AS avg_quantity
        FROM receivers r
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY r.Name;
    """,
    "Most claimed meal type": """
        SELECT f.Meal_Type, COUNT(c.Claim_ID) AS total_claims
        FROM claims c 
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Meal_Type 
        ORDER BY total_claims DESC;
    """,
    "Total quantity donated by each provider": """
        SELECT p.Name, SUM(f.Quantity) AS total_donated
        FROM providers p
        JOIN food_listings f ON p.Provider_ID = f.Provider_ID
        GROUP BY p.Name 
        ORDER BY total_donated DESC;
    """,
    "Claims summary by city": """
        SELECT f.Location, COUNT(c.Claim_ID) AS total_claims
        FROM claims c 
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Location 
        ORDER BY total_claims DESC;
    """
}

# --- Execute and display each query ---
for title, query in queries.items():
    print(f"\n=== {title} ===")
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = cursor.column_names
    df = pd.DataFrame(rows, columns=columns)
    print(df)

cursor.close()
conn.close()
import streamlit as st

st.title("Local Food Wastage Management System")
st.write("If you see this page in your browser, Streamlit is working!")
