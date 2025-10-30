
Credit Score Prediction Dashboard

This is a machine learning project that predicts a customer's credit score category (Poor, Standard, or Good) based on their financial data. The project includes a data cleaning and model training pipeline (train.py) and an interactive web dashboard (app.py) built with Streamlit.

(Note: You'll need to upload image_8872dd.png to your GitHub repo for this image to show)

Project Structure

app.py: The Streamlit web application.

train.py: The script to clean data and train the Random Forest model.

requirements.txt: A list of all Python libraries required.

.gitignore: Specifies files for Git to ignore (data, models, etc.).

🚀 How to Run This Project

1. Clone the Repository

git clone [https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git)
cd YOUR-REPOSITORY-NAME


2. Set Up a Virtual Environment (Recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


3. Install Dependencies

pip install -r requirements.txt


4. Get the Data
This repository does not store the creditscore.csv data file. You must add it to the main project folder.

5. Train the Model
You must run the training script first to generate the credit_score_model.pkl and scaler.pkl files:

python train.py


6. Run the Streamlit App
Once the model files are generated, run the Streamlit app:

streamlit run app.py
