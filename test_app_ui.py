from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_credit_app_ui():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # Essential for running on Jenkins agents
    
    # Initialize the WebDriver Interface
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("http://localhost:8501")
        time.sleep(5)
        
        # Verify Page Title
        assert "Credit" in driver.title
        print("Success: Title verification passed!")

        # Verify Header exists using a Locator
        header = driver.find_element(By.TAG_NAME, "h1")
        print(f"Success: Found Header: {header.text}")
        
    finally:
        driver.quit() # Close browser session

if __name__ == "__main__":
    test_credit_app_ui()