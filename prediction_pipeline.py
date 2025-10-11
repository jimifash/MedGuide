import joblib
import pandas as pd

# Load saved preprocessor and model
preprocessor = joblib.load("preprocessor.pkl")
model = joblib.load("disease_predictor.pkl")

def process_prediction(file_path, preprocessor=preprocessor, model=model):
    # Read and clean new patient data
    new_patient = pd.read_csv(file_path)
    new_patient = new_patient.loc[:, ~new_patient.columns.str.contains('^Unnamed')]

    # Ensure the columns match what the preprocessor expects
    if hasattr(preprocessor, "feature_names_in_"):
        expected_cols = list(preprocessor.feature_names_in_)
        new_patient = new_patient[expected_cols]

    # Pass a DataFrame (not NumPy) to the preprocessor
    X_new = preprocessor.transform(new_patient)

    # Convert transformed data to DataFrame (optional, for debugging)
    try:
        encoded_feature_names = preprocessor.get_feature_names_out()
        X_new_df = pd.DataFrame(X_new, columns=encoded_feature_names)
    except Exception:
        X_new_df = pd.DataFrame(X_new)

    # Predict
    prediction = model.predict(X_new)

    return X_new_df, prediction
