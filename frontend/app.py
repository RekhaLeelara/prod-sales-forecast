import streamlit as st
import pandas as pd
import requests

BACKEND_URL = "http://backend:7860"

st.title("SuperKart Product Sales Forecast App")
st.write("Predict product sales based on key product and store features.")

# Load dataset to populate selectboxes
df = pd.read_csv("SuperKart.csv")

# Numeric sliders (ranges based on typical retail values; adjust if needed)
Product_Weight = st.slider("Product Weight", 4.0, 22.0, 50.0)
Product_Sugar_Content = st.slider("Product Sugar Content", 0.0, 100.0, 10.0)
Product_Allocated_Area = st.slider("Product Allocated Area", 0.004, 2000.0, 100.0)
Product_MRP = st.slider("Product MRP", 0.0, 5000.0, 100.0)
Store_Establishment_Year = st.slider("Store Establishment Year", 1950, 2025, 2000)

# Categorical selectboxes (values taken directly from your dataset)
Product_Id = st.selectbox("Product ID", df["Product_Id"].unique())
Product_Type = st.selectbox("Product Type", df["Product_Type"].unique())
Store_Id = st.selectbox("Store ID", df["Store_Id"].unique())
Store_Size = st.selectbox("Store Size", df["Store_Size"].unique())
Store_Location_City_Type = st.selectbox("Store Location City Type", df["Store_Location_City_Type"].unique())
Store_Type = st.selectbox("Store Type", df["Store_Type"].unique())

# Build input JSON
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
    "Store_Type": Store_Type
}

# Prediction button
if st.button("Predict", type='primary'):
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data)

    if response.status_code == 200:
        result = response.json()
        predicted_sales = result["Predicted_Sales"]
        st.success(f"Predicted Sales Forecast: **{predicted_sales:.2f}**")
    else:
        st.error("Error in API request")

# Batch Prediction
st.subheader("Batch Prediction")
file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    if st.button("Predict for Batch", type='primary'):
        response = requests.post(
            f"{BACKEND_URL}/v1/salesbatch",
            files={"file": file}
        )

        if response.status_code == 200:
            result = response.json()
            st.header("Batch Prediction Results")
            st.write(result)
        else:
            st.error("Error in API request")

print(Product_Id)
