from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def run_selenium_test():
    # Setup for Jenkins (Headless mode)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    
    # Initialize Driver 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Navigate to Application 
        driver.get("http://localhost:8501")
        time.sleep(5) # Wait for Streamlit to render
        
        # 1. Verify Page Title 
        print("Page Title is:", driver.title)
        assert "Credit" in driver.title
        
        # 2. Find and Verify Main Header 
        header = driver.find_element(By.TAG_NAME, "h1")
        print("Found Header:", header.text)
        assert len(header.text) > 0
        
        print("Selenium UI Test Passed Successfully!")
        
    except Exception as e:
        print("Test Failed:", e)
        exit(1)
    finally:
        # Close Browser 
        driver.quit()

if __name__ == "__main__":
    run_selenium_test()
