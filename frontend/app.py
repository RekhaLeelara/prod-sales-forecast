import os

import pandas as pd
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:7860")

st.title("SuperKart Product Sales Forecast App")
st.write("Predict product sales based on key product and store features.")

# Load dataset to populate the dropdowns
df = pd.read_csv("SuperKart.csv")

# Numeric inputs: ranges and defaults taken from the training data
Product_Weight = st.slider("Product Weight", 4.0, 22.0, 12.65)
Product_Allocated_Area = st.slider("Product Allocated Area", 0.004, 0.298, 0.056, step=0.001)
Product_MRP = st.slider("Product MRP", 31.0, 266.0, 146.7)
Store_Establishment_Year = st.slider("Store Establishment Year", 1987, 2009, 2009)

# Categorical inputs
Product_Id = st.selectbox("Product ID", df["Product_Id"].unique())
Product_Sugar_Content = st.selectbox("Product Sugar Content", df["Product_Sugar_Content"].unique())
Product_Type = st.selectbox("Product Type", df["Product_Type"].unique())
Store_Id = st.selectbox("Store ID", df["Store_Id"].unique())
Store_Size = st.selectbox("Store Size", df["Store_Size"].unique())
Store_Location_City_Type = st.selectbox("Store Location City Type", df["Store_Location_City_Type"].unique())
Store_Type = st.selectbox("Store Type", df["Store_Type"].unique())

input_data = {
    "Product_Id": Product_Id,
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_Type": Product_Type,
    "Product_MRP": Product_MRP,
    "Store_Id": Store_Id,
    "Store_Establishment_Year": Store_Establishment_Year,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
}

if st.button("Predict", type="primary"):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data, timeout=15)
        if response.status_code == 200:
            predicted = response.json()["Predicted_Sales"]
            st.success(f"Predicted Sales Forecast: **{predicted:.2f}**")
        else:
            st.error(f"API error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not reach the backend at {BACKEND_URL}: {e}")

st.subheader("Batch Prediction")
file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None and st.button("Predict for Batch", type="primary"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/salesforecast",
            files={"file": (file.name, file.getvalue(), "text/csv")},
            timeout=60,
        )
        if response.status_code == 200:
            st.header("Batch Prediction Results")
            st.dataframe(pd.DataFrame(response.json()))
        else:
            st.error(f"API error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not reach the backend at {BACKEND_URL}: {e}")
