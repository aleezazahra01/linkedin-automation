# Pre-requisites
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class LinkedinAutomation:
    def __init__(self, data):
        self.email = data['email']
        self.password = data['password']
        self.file_path = data['file_path']
        self.phone_number = data['phone_number']
        self.keywords = data['keywords']
        self.location = data['location']
        self.current_salary = data['current_salary']

        # Chrome setup
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get('https://linkedin.com/')
        time.sleep(4)

    def login(self):
        # Click login button
        login = self.driver.find_element(By.CSS_SELECTOR, 'a[data-test-id="home-hero-sign-in-cta"]')
        login.click()

        login_email = self.driver.find_element(By.NAME, 'session_key')
        login_email.clear()
        login_email.send_keys(self.email)

        login_password = self.driver.find_element(By.NAME, 'session_password')
        login_password.clear()
        login_password.send_keys(self.password)

        login_email.send_keys(Keys.RETURN)
        print("Logged in successfully.")
        time.sleep(3)

    def job_search(self):
        # Go to Jobs section
        job_btn = self.driver.find_element(By.XPATH, "//a[@href='/jobs/']")
        job_btn.click()

        # Wait for search bar
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search jobs"]'))
        )

        search_bar = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search jobs"]')
        search_bar.clear()
        search_bar.click()
        search_bar.send_keys(self.keywords)

        # Enter location
        location_sb = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search location"]')
        location_sb.clear()
        location_sb.send_keys(self.location)
        location_sb.send_keys(Keys.ENTER)

        # Wait for filter bar
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'search-reusables__filters-bar'))
        )

        # Click Easy Apply filter
        try:
            easy_apply = self.driver.find_element(By.XPATH, '//button[contains(@aria-label,"Easy Apply")]')
            easy_apply.click()
        except:
            print("Easy Apply filter not found.")
        time.sleep(5)

    def apply(self):
        while True:
            # Wait until job listings load
            job_cards = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'jobs-search-results__list-item'))
            )
            print(f"Found {len(job_cards)} jobs on this page")

            for i, job in enumerate(job_cards):
                try:
                    job.click()
                    time.sleep(2)

                    # Check if Easy Apply button exists
                    try:
                        ea_bttn = self.driver.find_element(By.XPATH, '//button[contains(@aria-label,"Easy Apply")]')
                        ea_bttn.click()
                    except:
                        print(f"Job {i + 1}: No Easy Apply button, skipping...")
                        continue

                    # Fill phone number
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="phoneNumber"]'))
                    )
                    mobile_number = self.driver.find_element(By.CSS_SELECTOR, 'input[name="phoneNumber"]')
                    mobile_number.clear()
                    mobile_number.send_keys(self.phone_number)

                    # Click Next
                    next_btn = self.driver.find_element(By.XPATH, '//button[contains(@aria-label,"Continue")]')
                    next_btn.click()
                    time.sleep(2)

                    # Upload resume
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
                    )
                    upload_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
                    upload_input.send_keys(self.file_path)
                    time.sleep(3)

                    # Click next again (if exists)
                    try:
                        nxt_btn2 = self.driver.find_element(By.XPATH, '//button[contains(@aria-label,"Continue")]')
                        nxt_btn2.click()
                    except:
                        pass

                    # Current salary input (if required)
                    try:
                        salary_input = self.driver.find_element(By.XPATH, '//input[contains(@name,"salary")]')
                        salary_input.clear()
                        salary_input.send_keys(self.current_salary)
                    except:
                        print("Salary input not required for this job")

                    # Review and Submit
                    try:
                        review_btn = self.driver.find_element(By.XPATH, '//button[contains(@aria-label,"Review your application")]')
                        review_btn.click()
                    except:
                        pass

                    submit_application = self.driver.find_element(By.XPATH, '//button[contains(@aria-label,"Submit application")]')
                    submit_application.click()
                    print(f"Job {i + 1}: Application submitted successfully")
                    time.sleep(2)

                except Exception as e:
                    print(f"Error applying for job {i + 1}: {str(e)}")
                    continue

            # Handle pagination
            try:
                next_btn = self.driver.find_element(By.XPATH, '//button[@aria-label="Next"]')
                if next_btn.is_enabled():
                    next_btn.click()
                    time.sleep(5)
                else:
                    print("No more pages available")
                    break
            except:
                print("Next button not found, ending process.")
                break


if __name__ == '__main__':
    data = {
        'email': 'your_email_here',
        'password': 'your_password_here',
        'file_path': r'C:\path\to\resume.pdf',
        'phone_number': '03001234567',
        'keywords': 'Python Developer',
        'location': 'Pakistan',
        'current_salary': '100000'
    }

    bot = LinkedinAutomation(data)
    bot.login()
    bot.job_search()
    bot.apply()
