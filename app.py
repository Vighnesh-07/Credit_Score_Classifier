# app.py (Corrected and Refined with 3 Categories)

import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Credit Score Report",
    page_icon="📊",
    layout="wide"
)

# --- Custom CSS for a professional, modern look ---
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem; padding-bottom: 2rem;
        padding-left: 5rem; padding-right: 5rem;
    }
    .stButton>button {
        background-color: #2DA291; color: white;
        border-radius: 0.5rem; height: 3rem; font-weight: bold;
    }
    /* Custom container for cards */
    .card {
        background-color: #1a222e; border: 1px solid #2e3b4e;
        border-radius: 0.5rem; padding: 1.5rem;
        margin-bottom: 1.5rem; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        height: 100%; /* Ensure cards in the same row have equal height */
    }
    .card-title {
        font-size: 1.25rem; font-weight: bold;
        margin-bottom: 1rem; color: #a1aab7;
    }
    /* Ensure table text is visible in dark mode */
    table {
        color: white;
    }
    th {
        color: #a1aab7; /* Lighter color for table headers */
    }
</style>
""", unsafe_allow_html=True)

# --- Load Model, Scaler, and Feature Names ---
@st.cache_resource
def load_assets():
    """Loads the trained model, scaler, and feature names."""
    try:
        model = joblib.load('credit_score_model.pkl')
        scaler = joblib.load('scaler.pkl')
        # This list MUST match the 'features' list in train.py EXACTLY
        features = [
            'Age', 'Annual_Income', 'Monthly_Inhand_Salary', 'Num_of_Loan',
            'Delay_from_due_date', 'Num_of_Delayed_Payment', 'Changed_Credit_Limit',
            'Credit_Mix', 'Outstanding_Debt', 'Credit_Utilization_Ratio',
            'Credit_History_Age', 'Payment_of_Min_Amount', 'Amount_invested_monthly',
            'Monthly_Balance'
        ]
        return model, scaler, features
    except FileNotFoundError:
        st.error("Model assets (`credit_score_model.pkl` or `scaler.pkl`) not found. Please run `train.py` first.")
        return None, None, None
    except Exception as e:
        st.error(f"An error occurred loading model assets: {e}")
        return None, None, None

model, scaler, feature_names = load_assets()

# --- Helper Functions ---
def get_score_category_and_color(score_category_index):
    if score_category_index == 0: return "Poor", "🟥", "#E76258" # Red
    if score_category_index == 1: return "Standard", "🟨", "#F8A137" # Orange/Yellow
    if score_category_index == 2: return "Good", "🟩", "#2DA291" # Green
    return "Unknown", "❔", "#A1AAB7" # Default case

def interpret_factor_impact(feature_name, value):
    if feature_name == 'Credit_Utilization_Ratio':
        if value > 50: return "🟥 Very High - Strong Negative Impact"
        if value > 30: return "🟧 High - Negative Impact"
        if value < 10: return "✅ Very Low - Strong Positive Impact"
        return "🟩 Good - Positive Impact"
    if feature_name == 'Num_of_Delayed_Payment':
        if value > 5: return "🟥 High - Strong Negative Impact"
        if value > 1: return "🟧 Moderate - Negative Impact"
        return "🟩 Excellent - Strong Positive Impact"
    if feature_name == 'Credit_History_Age':
        if value < 36: return "🟧 Short - Moderate Negative Impact"
        if value > 120: return "✅ Long - Strong Positive Impact"
        return "🟩 Good - Positive Impact"
    if feature_name == 'Outstanding_Debt':
        # Simple check, could be refined with income ratio if desired
        if value > 5000: return "🟧 High - Potential Negative Impact"
        if value < 500: return "🟩 Low - Positive Impact"
        return "🟨 Moderate"
    # Default for unlisted factors
    return "Neutral"


# --- Main Page Layout ---
st.title("Your Credit Score Prediction")
st.markdown("Based on your financial details, here’s your estimated credit score and insights.")

# --- Input Form on Main Page ---
with st.form(key='user_input_form'):
    st.header("Enter Your Financial Details")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("👤 Personal & Income")
        age = st.number_input('Age', 18, 100, 30, help="Your current age.")
        annual_income = st.number_input('Annual Income ($)', 5000.0, 500000.0, 60000.0, 1000.0, help="Your total income before taxes.")
        monthly_inhand_salary = st.number_input('Monthly In-hand Salary ($)', 400.0, 30000.0, 4000.0, 100.0, help="Salary after taxes and deductions.")

    with col2:
        st.subheader("💳 Debts & Assets")
        outstanding_debt = st.number_input('Outstanding Debt ($)', 0.0, 50000.0, 2500.0, 100.0, help="Total amount owed across all credit lines.")
        monthly_balance = st.number_input('Average Monthly Balance ($)', 0.0, 20000.0, 800.0, 50.0, help="Typical end-of-month balance in checking/savings.")
        amount_invested_monthly = st.number_input('Amount Invested Monthly ($)', 0.0, 10000.0, 300.0, 10.0, help="Regular monthly investments.")

    with col3:
        st.subheader("📜 Credit History & Behavior")
        num_of_loan = st.slider('Number of Loans', 0, 15, 4, help="Total count of active loans (auto, home, personal etc.).")
        num_of_delayed_payment = st.slider('Number of Delayed Payments', 0, 30, 3, help="How many times have payments been late historically.")
        delay_from_due_date = st.slider('Average Days Delayed from Due Date', 0, 60, 12, help="Typical delay when payments are late.")
        credit_utilization_ratio = st.slider('Credit Utilization Ratio (%)', 0.0, 100.0, 45.0, 1.0, help="Percentage of available credit you are using (e.g., on credit cards).")
        credit_history_age = st.number_input('Credit History Age (months)', 1, 600, 72, help="How long you've had credit accounts (in months).")
        changed_credit_limit = st.number_input('Changed Credit Limit', 0.0, 50.0, 10.0, 0.5, help="Change in credit limit over a period.")
        payment_of_min_amount = st.selectbox('Pays Only Minimum Amount?', ('No', 'Yes'), help="Do you typically pay only the minimum on credit cards?")
        credit_mix = st.selectbox('Credit Mix', ('Good', 'Standard', 'Bad'), help="Variety of credit types (cards, loans etc.).")

    submit_button = st.form_submit_button(label="Generate My Report")

# --- Display Output Section ---
if submit_button and all(assets is not None for assets in [model, scaler, feature_names]):
    st.markdown("---") # Visual separator

    # --- Data Preparation & Prediction ---
    credit_mix_map = {'Bad': 1, 'Standard': 2, 'Good': 3}
    payment_map = {'Yes': 1, 'No': 0}
    data = {
        'Age': age, 'Annual_Income': annual_income, 'Monthly_Inhand_Salary': monthly_inhand_salary,
        'Num_of_Loan': num_of_loan, 'Delay_from_due_date': delay_from_due_date,
        'Num_of_Delayed_Payment': num_of_delayed_payment, 'Changed_Credit_Limit': changed_credit_limit,
        'Credit_Mix': credit_mix_map[credit_mix], 'Outstanding_Debt': outstanding_debt,
        'Credit_Utilization_Ratio': credit_utilization_ratio / 100.0,
        'Credit_History_Age': credit_history_age, 'Payment_of_Min_Amount': payment_map[payment_of_min_amount],
        'Amount_invested_monthly': amount_invested_monthly, 'Monthly_Balance': monthly_balance
    }
    try:
        input_df = pd.DataFrame(data, index=[0])[feature_names]
    except KeyError as e:
        st.error(f"Missing expected feature during data preparation: {e}. Ensure train.py includes all necessary features.")
        st.stop()

    input_scaled = scaler.transform(input_df)

    # Get the primary prediction category (0, 1, or 2)
    prediction_cat_index = model.predict(input_scaled)[0]
    # Get prediction probabilities for all 3 classes
    prediction_proba = model.predict_proba(input_scaled)[0]

    # --- Calculate the final score based on probabilities ---
    score_weights = np.array([400, 600, 800]) # Example weights for Poor, Standard, Good
    predicted_score = int(np.dot(prediction_proba, score_weights))
    # Keep score within a reasonable display range (e.g., 300-850)
    predicted_score = max(300, min(850, predicted_score))

    # Get the category name, emoji, and color based on the *primary predicted category index*
    category, color_emoji, gauge_color = get_score_category_and_color(prediction_cat_index)

    # --- 1. Header & Score Summary ---
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<p class="card-title">Your Predicted Credit Score {color_emoji}</p>', unsafe_allow_html=True)
        # Display the calculated score number, but the gauge title uses the primary category
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", value = predicted_score,
            number = {'font': {'size': 60}},
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': category, 'font': {'size': 30}}, # Title shows Poor/Standard/Good
            gauge = {
                'axis': {'range': [300, 850], 'tickwidth': 1, 'tickcolor': "darkgrey"},
                'bar': {'color': gauge_color}, # Bar color matches the category
                # Simplified steps for 3 categories
                'steps': [
                    {'range': [300, 500], 'color': '#1a222e'}, # Poor range approx
                    {'range': [500, 700], 'color': '#2e3b4e'}, # Standard range approx
                    {'range': [700, 850], 'color': '#1a222e'}], # Good range approx
                 'threshold' : {'line': {'color': "orange", 'width': 4}, 'thickness': 0.75, 'value': 500} # Example threshold
                }
            ))
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">💡 Recommendations</p>', unsafe_allow_html=True)
        recs_count = 0
        if credit_utilization_ratio > 30:
            st.warning("📉 **Reduce Credit Utilization:** Aim to keep your usage below 30% of your available credit.")
            recs_count += 1
        if num_of_delayed_payment > 1:
            st.warning("📅 **Prioritize On-Time Payments:** Payment history is crucial. Set reminders or auto-pay.")
            recs_count += 1
        if credit_history_age < 84:
            st.info("⏳ **Build Credit History:** Keep older, well-managed accounts open to lengthen your history.")
            recs_count += 1
        if recs_count == 0:
            st.success("✅ **Keep it Up!** Your key credit factors look strong. Maintain these positive habits.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. Credit Factors Overview & Visual Analytics ---
    col3, col4 = st.columns([1, 1])
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">📊 Key Factors Overview</p>', unsafe_allow_html=True)
        overview_data = {
            "Factor": ["Credit Utilization", "Delayed Payments", "Credit History Age", "Outstanding Debt"],
            "Your Value": [f"{credit_utilization_ratio:.0f}%", num_of_delayed_payment, f"{credit_history_age} months", f"${outstanding_debt:,.0f}"],
            "Impact Assessment": [
                interpret_factor_impact('Credit_Utilization_Ratio', credit_utilization_ratio),
                interpret_factor_impact('Num_of_Delayed_Payment', num_of_delayed_payment),
                interpret_factor_impact('Credit_History_Age', credit_history_age),
                interpret_factor_impact('Outstanding_Debt', outstanding_debt)
            ]
        }
        st.table(pd.DataFrame(overview_data))
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">📈 General Feature Importance</p>', unsafe_allow_html=True)
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances}).sort_values('importance', ascending=False).head(5)
            fig_bar = go.Figure(go.Bar(x=importance_df['importance'], y=importance_df['feature'], orientation='h', marker_color='#2DA291'))
            fig_bar.update_layout(title="Top 5 Factors Influencing Scores (General)", yaxis=dict(autorange="reversed"), height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Feature importance data is not available for this model type.")
        st.markdown('</div>', unsafe_allow_html=True)

elif not submit_button:
    st.info("Please fill in your complete profile above and click 'Generate My Report' to get your personalized credit health analysis.")
elif submit_button and (model is None or scaler is None or feature_names is None):
     st.error("Could not generate report because model assets failed to load. Please check the error message above.")

