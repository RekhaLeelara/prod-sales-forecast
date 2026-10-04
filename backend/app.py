import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the trained pipeline (scaler + regressor) saved from the notebook
model = joblib.load("superkart_model.joblib")

# Columns the pipeline was fitted on (target column is not included)
FEATURE_COLUMNS = list(
    getattr(model, "feature_names_in_", [
        "Product_Id", "Product_Weight", "Product_Sugar_Content",
        "Product_Allocated_Area", "Product_Type", "Product_MRP", "Store_Id",
        "Store_Establishment_Year", "Store_Size", "Store_Location_City_Type",
        "Store_Type",
    ])
)

# The notebook's preprocessor only scales these numeric columns
REQUIRED_NUMERIC = [
    "Product_Weight", "Product_Allocated_Area",
    "Product_MRP", "Store_Establishment_Year",
]


@app.get("/")
def home():
    return "Welcome to the Sales Forecast Prediction API!"


@app.post("/v1/sales")
def predict_sales():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    missing = [c for c in REQUIRED_NUMERIC if c not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # Keep columns in training order; ignore any extra keys
    input_df = pd.DataFrame([data]).reindex(columns=FEATURE_COLUMNS)
    prediction = float(model.predict(input_df)[0])
    return jsonify({"Predicted_Sales": prediction})


@app.post("/v1/salesforecast")
def predict_sales_batch():
    if "file" not in request.files:
        return jsonify({"error": "Upload a CSV under the key 'file'"}), 400

    df = pd.read_csv(request.files["file"])
    input_df = df.reindex(columns=FEATURE_COLUMNS)
    df["Predicted_Sales"] = model.predict(input_df).tolist()
    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
