from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import time

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get credentials from environment variables
    USERNAME = os.getenv("MOODLE_USERNAME")
    PASSWORD = os.getenv("MOODLE_PASSWORD")

    # Validate credentials
    if not USERNAME or not PASSWORD:
        raise ValueError("Please ensure MOODLE_USERNAME and MOODLE_PASSWORD are correctly set in the .env file")

    print("Starting browser and logging into NTNU Moodle System...")
    
    with sync_playwright() as p:
        # Launch browser with automation detection disabled
        browser = p.chromium.launch(
            headless=False, 
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        # Create a new browser context
        context = browser.new_context()
        
        # Create a new page
        page = context.new_page()

        # Navigate to the Moodle login page
        page.goto("https://moodle3.ntnu.edu.tw")
        print("Navigated to Moodle login page")
        
        # Wait for the page to load
        page.wait_for_timeout(3000)
        
        # Take screenshot before login
        page.screenshot(path="before_login.png")
        print("Captured pre-login screenshot")

        # Fill in login credentials
        page.fill("#username", USERNAME)
        page.fill("#password", PASSWORD)
        
        # Try pressing Enter on the password field instead of clicking a button
        print("Submitting login form by pressing Enter...")
        page.press("#password", "Enter")
        
        # Wait for navigation to complete
        page.wait_for_load_state("networkidle")
        
        # Take screenshot after login
        page.screenshot(path="after_login.png")
        print("Login successful!")
        
        # Navigate to the Data Structure course page
        page.goto("https://moodle3.ntnu.edu.tw/course/view.php?id=47767")
        page.wait_for_timeout(3000)
        print("Accessed 1132 Data Structure course")
        
        # Take screenshot of the course page
        page.screenshot(path="course_opened.png")
        print("Course page screenshot captured")

        # Keep the browser open for debugging
        print("\nBrowser will remain open. Press Enter to close...")
        input()
        
        # Close the browser
        browser.close()
        print("Browser closed")

if __name__ == "__main__":
    main()
