import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

def preprocess(df):
    categorical_cols = ['Gender']
    numeric_scale_cols = ['Age', 'Fever', 'Symptom_Duration_Days']
    binary_cols = [
        'Cough', 'Headache', 'Fatigue', 'Nausea', 'Muscle_Pain',
        'Shortness_of_Breath', 'Loss_of_Taste', 'Abdominal_Pain',
        'Appetite_Loss', 'Frequent_Urination', 'Thirst_Level',
        'Blurred_Vision', 'Severity(1-5)'
    ]

    # --- Define preprocessors ---
    categorical_transformer = OneHotEncoder(drop='first', sparse_output=False)
    numeric_transformer = StandardScaler()

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_cols),
            ('num', numeric_transformer, numeric_scale_cols),
            ('binary', 'passthrough', binary_cols)
        ]
    )

    # --- Fit and transform training data ---
    X = df.drop(columns=['Patient_ID'])
    X_preprocessed = preprocessor.fit_transform(X)

    # --- Save the preprocessor ---
    joblib.dump(preprocessor, "preprocessor.pkl")


def train_store_model(df, preprocessors, save_path="disease_predictor.pkl"):

    X = df.drop(columns=['Patient_ID', 'Disease'])
    y = df['Disease']
    
    model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        n_estimators=200, random_state=42, class_weight='balanced'
        ))
    ])

    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
    )


    model.fit(X_train, y_train)
    joblib.dump(model, save_path)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    return acc

df = pd.read_csv("realistic_patient_symptom_features")
preprocess(df)
preprocessors = joblib.load("preprocessor.pkl")
accuracy = train_store_model(df,preprocessors)