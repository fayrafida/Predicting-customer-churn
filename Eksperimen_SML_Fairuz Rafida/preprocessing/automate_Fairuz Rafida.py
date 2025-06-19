import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocess_telco_data(csv_path):
    # Load data
    df = pd.read_csv(csv_path)

    # Konversi TotalCharges ke numerik
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Daftar kolom yang memiliki dua nilai: 'Yes'/'No' atau 'True'/'False'
    yes_no_columns = [
        col for col in df.columns
        if df[col].dropna().nunique() <= 2 and set(df[col].dropna().unique()).issubset({'Yes', 'No', 'True', 'False'})
    ]

    # Mengubah ke tipe boolean
    for col in yes_no_columns:
        df[col] = df[col].map({'Yes': True, 'No': False, 'True': True, 'False': False})

    
    # Buang kolom yang tidak diperlukan
    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])

    categorical_columns = [
        'gender', 'SeniorCitizen', 'Partner', 'Dependents',
        'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies',
        'Contract', 'PaperlessBilling', 'PaymentMethod', 'Churn'
    ]

    if 'customerID' in categorical_columns:
        categorical_columns.remove('customerID')

    # One-hot encoding pada kolom kategorikal
    df_encoded = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

    # Pilih fitur numerik
    numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']

    # Drop baris dengan nilai kosong (jika ada)
    df_encoded = df_encoded.dropna(subset=numerical_features)

    # Normalisasi (Min-Max Scaling) ===
    min_max_scaler = MinMaxScaler()
    df_normalized = df_encoded.copy()
    df_normalized[numerical_features] = min_max_scaler.fit_transform(df_encoded[numerical_features])

    # Drop baris dengan nilai kosong (jika ada)
    df_encoded = df_encoded.dropna(subset=numerical_features)

    # Normalisasi (Min-Max Scaling) ===
    min_max_scaler = MinMaxScaler()
    df_normalized = df_encoded.copy()
    df_normalized[numerical_features] = min_max_scaler.fit_transform(df_encoded[numerical_features])

    return df_normalized
