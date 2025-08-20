import pandas as pd
import streamlit as st

# --- Load data from CSV files ---
providers = pd.read_csv("providers.csv")
receivers = pd.read_csv("receivers.csv")
food_listings = pd.read_csv("food_listings.csv")
claims = pd.read_csv("claims.csv")

# --- Streamlit App ---
st.title("Local Food Wastage Management System")

# Display raw data previews
st.subheader("Providers Data")
st.dataframe(providers.head())

st.subheader("Receivers Data")
st.dataframe(receivers.head())

st.subheader("Food Listings Data")
st.dataframe(food_listings.head())

st.subheader("Claims Data")
st.dataframe(claims.head())


# --- Recreate query outputs using pandas instead of SQL ---
st.subheader("Providers count by city")
st.dataframe(providers.groupby("City").size().reset_index(name="total_providers"))

st.subheader("Top provider types")
st.dataframe(providers.groupby("Type").size().reset_index(name="total").sort_values("total", ascending=False))

st.subheader("Provider contact info (Delhi)")
st.dataframe(providers[providers["City"] == "Delhi"][["Name", "Contact"]])

st.subheader("Receivers count by city")
st.dataframe(receivers.groupby("City").size().reset_index(name="total_receivers"))

st.subheader("Receivers with most claims")
st.dataframe(
    claims.merge(receivers, on="Receiver_ID")
          .groupby("Name").size()
          .reset_index(name="total_claims")
          .sort_values("total_claims", ascending=False)
)

st.subheader("Total food quantity available")
st.write(food_listings["Quantity"].sum())

st.subheader("Cities with highest food listings")
st.dataframe(food_listings.groupby("Location").size().reset_index(name="total_listings").sort_values("total_listings", ascending=False))

st.subheader("Most common food types")
st.dataframe(food_listings.groupby("Food_Type").size().reset_index(name="total_items").sort_values("total_items", ascending=False))

st.subheader("Claims count for each food item")
st.dataframe(
    claims.merge(food_listings, on="Food_ID")
          .groupby("Food_Name").size()
          .reset_index(name="total_claims")
)

st.subheader("Provider with highest successful claims")
st.dataframe(
    claims[claims["Status"] == "Completed"]
          .merge(food_listings, on="Food_ID")
          .merge(providers, on="Provider_ID")
          .groupby("Name").size()
          .reset_index(name="successful_claims")
          .sort_values("successful_claims", ascending=False)
)

st.subheader("Claim status distribution")
st.dataframe(claims.groupby("Status").size().reset_index(name="total_claims"))

st.subheader("Average quantity claimed per receiver")
st.dataframe(
    claims.merge(food_listings, on="Food_ID")
          .merge(receivers, on="Receiver_ID")
          .groupby("Name")["Quantity"].mean()
          .reset_index(name="avg_quantity")
)

st.subheader("Most claimed meal type")
st.dataframe(
    claims.merge(food_listings, on="Food_ID")
          .groupby("Meal_Type").size()
          .reset_index(name="total_claims")
          .sort_values("total_claims", ascending=False)
)

st.subheader("Total quantity donated by each provider")
st.dataframe(
    food_listings.merge(providers, on="Provider_ID")
                 .groupby("Name")["Quantity"].sum()
                 .reset_index(name="total_donated")
                 .sort_values("total_donated", ascending=False)
)

st.subheader("Claims summary by city")
st.dataframe(
    claims.merge(food_listings, on="Food_ID")
          .groupby("Location").size()
          .reset_index(name="total_claims")
          .sort_values("total_claims", ascending=False)
)
