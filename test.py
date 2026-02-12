from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize Chrome Driver
driver = webdriver.Chrome()

try:
    # 1. Open the Streamlit App
    driver.get("http://localhost:8501")
    time.sleep(3)  # Wait for Streamlit to load

    # 2. Find and fill input fields (Update IDs based on your app's inspect element)
    # Example: Annual Income field
    income_field = driver.find_element(By.XPATH, "//input[@aria-label='Annual_Income']")
    income_field.send_keys("50000")

    # Example: Number of Bank Accounts field
    accounts_field = driver.find_element(By.XPATH, "//input[@aria-label='Num_Bank_Accounts']")
    accounts_field.send_keys("3")

    # 3. Click the Predict Button
    predict_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Predict')]")
    predict_button.click()
    time.sleep(2)  # Wait for model processing

    # 4. Verify the Prediction Result appears
    # Replace 'Credit Score is' with whatever prefix your app uses for results
    result_text = driver.find_element(By.XPATH, "//*[contains(text(), 'Credit Score')]").text
    assert "Credit Score" in result_text
    print(f"Test Passed: Successfully detected output - {result_text}")

except Exception as e:
    print(f"Test Failed: {e}")

finally:
    # 5. Close the browser
    driver.quit()
