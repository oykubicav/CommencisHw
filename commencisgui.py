from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

# Setup ChromeDriver and Chrome Options
options = webdriver.ChromeOptions()
options.binary_location = "/Users/oykubicav/Downloads/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

# Disable third-party cookie restrictions and blink features
options.add_argument("--disable-site-isolation-trials")
options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize ChromeDriver with service and options
service = Service("/Users/oykubicav/Downloads/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# Open Commencis website
driver.get("https://www.commencis.com")

# Automatically dismiss notification permission pop-up
try:
    alert = Alert(driver)
    alert.dismiss()
except:
    print("No alert to dismiss.")

# Accept the cookie consent if the button exists
try:
    accept_cookies = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept All')]"))
    )
    accept_cookies.click()
except:
    print("No cookie banner appeared.")

# Increase timeout for waiting for the element to load
wait = WebDriverWait(driver, 20)

# Wait for the "Insights" element to appear using XPath
insights_menu = wait.until(
    EC.presence_of_element_located((By.XPATH, "//span[@class='gm-menu-item__txt' and text()='Insights']"))
)

# Hover over the "Insights" menu item
ActionChains(driver).move_to_element(insights_menu).perform()

# Wait for the "Blog" link and click it using the updated XPath
blogs_link = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='https://www.commencis.com/thoughts/' and .//span[text()='Blog']]"))
)
blogs_link.click()

# Verify that the Blogs page has loaded by checking the title contains 'Blog'
assert "Blog" in driver.title, "Failed to open Blogs page."

# Now, verify all blogs in the Popular section
blogs = driver.find_elements(By.CSS_SELECTOR, "div.tmb.tmb-iso")

for index, blog in enumerate(blogs):
    print(f"\nVerifying Blog {index + 1}...")

    # Verify Title
    try:
        title_element = blog.find_element(By.CSS_SELECTOR, "h3.t-entry-title a")
        title = title_element.text
        assert title != "", "Title is missing"
        print(f"Title: {title}")
        
        # Click on the blog link to open the detailed page
        blog_link = title_element.get_attribute("href")
        driver.execute_script("window.open('');")  # Open a new tab
        driver.switch_to.window(driver.window_handles[1])  # Switch to new tab
        driver.get(blog_link)  # Open the blog page
        
        # Verify content inside the blog post
        print(f"Inside Blog: {title}")

        # Verify Stay Tuned Email Input (if available)
        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
            )
            print("Stay Tuned Email Input found.")
        except Exception as e:
            print("Stay Tuned Email Input not found:", str(e))

        # Verify Stay Tuned Button
        try:
            stay_tuned_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.wpcf7-submit"))
            )
            print("Stay Tuned Button found.")
        except Exception as e:
            print("Stay Tuned Button not found:", str(e))

        # Verify Author (if available)
        try:
            author_element = driver.find_element(By.CSS_SELECTOR, "h3.h4")
            author = author_element.text
            print(f"Author: {author}")
        except Exception as e:
            print("Error with author:", str(e))

        # Close the current tab and switch back to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print("Error with blog:", str(e))

print("Blog verification complete.")

# Close the browser after testing
driver.quit()
