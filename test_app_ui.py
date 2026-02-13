from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_ui():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # Required for Jenkins
    
    # Initialize WebDriver Interface
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Navigate to a stable live site for demonstration
        driver.get("https://www.google.com")
        time.sleep(3)
        
        # 1. Verify Title
        print("Page Title is:", driver.title)
        assert "Google" in driver.title
        
        # 2. Use a Locator to find the search box
        search_box = driver.find_element(By.NAME, "q")
        print("Success: Found search element using 'By.NAME' locator.")
        
        print("Experiment 6: Selenium UI Test PASSED!")
        
    finally:
        driver.quit() # Close browser session

if __name__ == "__main__":
    test_ui()
