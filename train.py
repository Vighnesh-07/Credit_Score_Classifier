# train.py
import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from scipy.stats import randint

# --- 1. Load Data ---
try:
    df = pd.read_csv('creditscore.csv', low_memory=False)
    print(f" Data loaded successfully. Initial shape: {df.shape}")
except FileNotFoundError:
    print(" Error: 'creditscore.csv' not found. Please ensure the file is in the correct directory.")
    exit()

# --- 2. Data Cleaning and Preprocessing ---
df.drop(columns=["ID", "Customer_ID", "SSN", "Name", "Month", "Payment_Behaviour"], inplace=True, errors='ignore')

for col in ['Occupation', 'Credit_Mix', 'Payment_of_Min_Amount', 'Type_of_Loan']:
    if col in df.columns:
        df[col] = df[col].astype(str)
        if col == 'Occupation': df[col] = df[col].replace('_______', 'Unknown')
        if col == 'Credit_Mix': df[col] = df[col].replace('_', 'Standard')
        if col == 'Payment_of_Min_Amount': df[col] = df[col].replace('NM', 'Not_Mentioned')

if 'Type_of_Loan' in df.columns:
    df.drop('Type_of_Loan', axis=1, inplace=True)

numeric_like_cols = [
    'Annual_Income', 'Num_of_Loan', 'Changed_Credit_Limit', 'Outstanding_Debt', 'Age',
    'Amount_invested_monthly', 'Monthly_Balance', 'Num_of_Delayed_Payment',
    'Monthly_Inhand_Salary', 'Num_Credit_Inquiries', 'Interest_Rate',
    'Num_Bank_Accounts', 'Num_Credit_Card'
]
for col in numeric_like_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

def convert_history_age(s):
    if not isinstance(s, str): return np.nan
    match = re.match(r'(\d+)\s*Years and (\d+)\s*Months', s)
    if match:
        years, months = map(int, match.groups())
        return years * 12 + months
    return np.nan
if 'Credit_History_Age' in df.columns:
    df['Credit_History_Age'] = df['Credit_History_Age'].apply(convert_history_age)

for col in df.select_dtypes(include=np.number).columns:
    df[col].fillna(df[col].median(), inplace=True)

if 'Age' in df.columns: df = df[(df['Age'] > 18) & (df['Age'] < 100)]
if 'Num_of_Loan' in df.columns: df = df[df['Num_of_Loan'] <= 15]
if 'Delay_from_due_date' in df.columns: df['Delay_from_due_date'] = df['Delay_from_due_date'].apply(lambda x: x if x >= 0 else 0)

print(f" Shape after cleaning: {df.shape}")

# --- 3. Feature Engineering and Encoding ---
if 'Credit_Mix' in df.columns: df['Credit_Mix'] = df['Credit_Mix'].map({'Bad': 1, 'Standard': 2, 'Good': 3})
if 'Payment_of_Min_Amount' in df.columns: df['Payment_of_Min_Amount'] = df['Payment_of_Min_Amount'].map({'Yes': 1, 'No': 0, 'Not_Mentioned': 2})

if 'Credit_Score' in df.columns:
    df['Credit_Score'] = df['Credit_Score'].map({'Poor': 0, 'Standard': 1, 'Good': 2})
    df.dropna(subset=['Credit_Score'], inplace=True)
    df['Credit_Score'] = df['Credit_Score'].astype(int)

print(f" Shape after encoding: {df.shape}")

# --- 4. Model Training & Hyperparameter Tuning ---
if df.empty:
    print("\n Error: DataFrame is empty. Cannot train model.")
    exit()

features = [
    'Age', 'Annual_Income', 'Monthly_Inhand_Salary', 'Num_of_Loan',
    'Delay_from_due_date', 'Num_of_Delayed_Payment', 'Changed_Credit_Limit',
    'Credit_Mix', 'Outstanding_Debt', 'Credit_Utilization_Ratio',
    'Credit_History_Age', 'Payment_of_Min_Amount', 'Amount_invested_monthly',
    'Monthly_Balance'
]
features = [f for f in features if f in df.columns]
X = df[features]
y = df['Credit_Score']

print(f"\n Starting model training with {X.shape[0]} samples.")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- Define Hyperparameter Search Space ---
param_dist = {
    'n_estimators': randint(100, 300),        
    'max_depth': [10, 20, 30, 40, None],   
    'min_samples_split': randint(2, 11),    
    'min_samples_leaf': randint(1, 6),      
    'max_features': ['sqrt', 'log2', None] 
}

# Create a base Random Forest model
rf = RandomForestClassifier(random_state=42)

rand_search = RandomizedSearchCV(
    estimator=rf,
    param_distributions=param_dist,
    n_iter=20, 
    cv=3,
    verbose=2,
    random_state=42,
    n_jobs=-1
)

print("Starting hyperparameter search...")
# Fit the random search to find the best parameters
rand_search.fit(X_train_scaled, y_train)

# Get the best model found by the search
best_rf_model = rand_search.best_estimator_
print(f"Best Hyperparameters found: {rand_search.best_params_}")

# Evaluate the *best* model on the test set
y_pred = best_rf_model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Fine-tuned model training complete. Accuracy: {accuracy:.2f}")

# --- 5. Save the Fine-Tuned Model and Scaler ---
joblib.dump(best_rf_model, 'credit_score_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("Fine-tuned model and scaler have been saved successfully.")
