# Install required libraries
# pip install pandas scikit-learn

# ============================================
# Pipe-and-Filter Pattern using
# Pima Indians Diabetes Dataset (from URL)
# File: diabetes_pipeline.py
# Run in VS Code
# ============================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# =========================================================
# DATASET URL
# =========================================================

DATASET_URL = (
    "https://raw.githubusercontent.com/"
    "jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
)

COLUMN_NAMES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome"
]


# =========================================================
# FILTER 1 : INPUT FILTER
# Reads dataset directly from URL
# =========================================================

def input_filter(url):

    print("\n[INPUT FILTER] Loading dataset from URL...")

    df = pd.read_csv(url, names=COLUMN_NAMES)

    print("\nDataset Shape:", df.shape)

    print("\nFirst 5 Records:")
    print(df.head())

    return df


# =========================================================
# FILTER 2 : DATA CLEANING FILTER
# Replace invalid 0 values with median
# =========================================================

def cleaning_filter(df):

    print("\n[CLEANING FILTER] Handling missing values...")

    columns = [
        'Glucose',
        'BloodPressure',
        'SkinThickness',
        'Insulin',
        'BMI'
    ]

    # Replace invalid zeros with NaN
    df[columns] = df[columns].replace(0, np.nan)

    # Show missing values before imputation
    print("\nMissing Values Before Imputation:")
    print(df[columns].isnull().sum())

    # Median imputation
    imputer = SimpleImputer(strategy='median')

    df[columns] = imputer.fit_transform(df[columns])

    # Show median values used
    print("\nMedian Values Used for Imputation:")

    for col, median in zip(columns, imputer.statistics_):
        print(f"{col}: {median}")

    # Show missing values after imputation
    print("\nMissing Values After Imputation:")
    print(df[columns].isnull().sum())

    print("\nFirst 5 Rows After Cleaning:")
    print(df.head())

    return df

# =========================================================
# FILTER 3 : FEATURE SCALING FILTER
# Standardize numeric features
# =========================================================

def scaling_filter(df):

    print("\n[SCALING FILTER] Scaling features...")

    X = df.drop("Outcome", axis=1)

    y = df["Outcome"]

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # Convert scaled array back to DataFrame
    scaled_df = pd.DataFrame(
        X_scaled,
        columns=X.columns
    )

    print("\nFirst 5 Rows After Scaling:")
    print(scaled_df.head())

    return X_scaled, y

# =========================================================
# FILTER 4 : MODEL TRAINING FILTER
# Train Logistic Regression model
# =========================================================

def training_filter(X, y):

    print("\n[TRAINING FILTER] Training Logistic Regression model...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = LogisticRegression()

    model.fit(X_train, y_train)

    print("Model training completed.")

    return model, X_test, y_test


# =========================================================
# FILTER 5 : OUTPUT FILTER
# Evaluate model performance
# =========================================================

def output_filter(model, X_test, y_test):

    print("\n[OUTPUT FILTER] Evaluating model...")

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("\nAccuracy Score:", round(accuracy, 4))

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))


# =========================================================
# PIPELINE EXECUTION
# Pipes transfer outputs between filters
# =========================================================

if __name__ == "__main__":

    # PIPE 1
    raw_data = input_filter(DATASET_URL)

    # PIPE 2
    cleaned_data = cleaning_filter(raw_data)

    # PIPE 3
    X_scaled, y = scaling_filter(cleaned_data)

    # PIPE 4
    model, X_test, y_test = training_filter(X_scaled, y)

    # PIPE 5
    output_filter(model, X_test, y_test)