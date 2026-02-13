from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_credit_app_ui():
    # 1. Setup Chrome Options (Headless for Jenkins)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    
    # 2. Initialize WebDriver Interface
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 3. Navigate to App URL
        driver.get("http://localhost:8501")
        time.sleep(5) # Wait for Streamlit rendering
        
        # 4. Assert Title (Testing different elements)
        assert "Credit" in driver.title
        print("Success: Title verification passed!")

        # 5. Use Locator to find Header
        header = driver.find_element(By.TAG_NAME, "h1")
        print(f"Success: Found Header: {header.text}")
        
    finally:
        # 6. Close Browser Session
        driver.quit()

if __name__ == "__main__":
    test_credit_app_ui()
