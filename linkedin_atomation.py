# Pre-requisites
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import re
import json
import configparser
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

        #  Updated ChromeDriver Setup
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")


        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get('https://www.linkedin.com/')
        time.sleep(4)

    def login(self):
        #click on the login with email 

        login = self.driver.find_element(By.CSS_SELECTOR, 'a[data-test-id="home-hero-sign-in-cta"]')
        login.click()

        login_email=self.driver.find_element(By.NAME, 'session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        time.sleep(3)
     
        login_password = self.driver.find_element(By.NAME, 'session_password')
        login_password.clear()
        login_password.send_keys(self.password)

        login_email.send_keys(Keys.RETURN)
        time.sleep(2)

    def job_search(self):
        # Go to the jobs section
    

        search_bar = self.driver.find_element(By.CSS_SELECTOR, 'input.search-global-typeahead__input')
        search_bar.click()

        # # Wait for search bar
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="jobs-search-box-keyword-id-ember1701"]'))
        # )
        # search_Bar = self.driver.find_element(By.XPATH, '//*[@id="jobs-search-box-keyword-id-ember1701"]')
        # search_Bar.clear()
        # search_Bar.click()

        # After clicking on the job bar send the keywords
        time.sleep(2)
        search_bar.send_keys(self.keywords)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(4)

        # Enter location
        # location_sb = self.driver.find_element(By.XPATH, '//*[@id="jobs-search-box-location-id-ember2040"]')
        # location_sb.clear()
        # location_sb.send_keys(self.location)
        # location_sb.send_keys(Keys.ENTER)
        #click on job filter

        job_filter =self.driver.find_element(By.XPATH,'//*[@id="search-reusables__filters-bar"]/ul/li[1]/button')
        job_filter.click()

        # Wait for filter bar
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="search-reusables__filters-bar"]/ul/li[1]'))
        )

        # Click on Easy Apply filter
        easy_apply = self.driver.find_element(By.XPATH, '//*[@id="search-reusables__filters-bar"]/ul/li[7]')
        easy_apply.click()
        time.sleep(5)

    def apply(self):
        # Wait until job listings load
        job_cards = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'jobs-search-results__list-item'))
        )

        print(f"Found {len(job_cards)} jobs on this page")

        for i, job in enumerate(job_cards):
            job.click()

            # Easy Apply button
            ea_bttn = self.driver.find_element(By.XPATH, '//*[@id="jobs-apply-button-id"]')
            ea_bttn.click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ember2707"]/div/div[2]/form/div/div'))
            )

            mobile_number = self.driver.find_element(By.CSS_SELECTOR, 'input[name="phoneNumber"]')
            mobile_number.clear()
            mobile_number.send_keys(self.phone_number)

            # Press Next button
            next_bttn = self.driver.find_element(By.XPATH, '//*[@id="ember2718"]')
            next_bttn.click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
            )

            # Upload resume
            upload_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
            upload_input.send_keys(self.file_path)
            time.sleep(3)

            nxt_bttn2 = self.driver.find_element(By.XPATH, '//*[@id="ember2718"]')
            nxt_bttn2.click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-4286652106-23243459210-numeric"]'))
            )

            crrnt_salary = self.driver.find_element(By.XPATH, '//*[@id="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-4286652106-23243459210-numeric"]')
            crrnt_salary.clear()
            crrnt_salary.send_keys(self.current_salary)

            # Review button
            review_bttn = self.driver.find_element(By.XPATH, '//*[@id="ember2744"]')
            review_bttn.click()
            time.sleep(3)

            # Submit application
            submit_application = self.driver.find_element(By.XPATH, '//*[@id="ember2754"]')
            submit_application.click()

if __name__ == '__main__':
    data = {
        'email': 'your_email_here',
        'password': 'your_password_here',
        'file_path': r'C:\path\to\resume.pdf',
        'phone_number': 'your_number_goes_here',
        'keywords': 'j*b_your_unemployed_ah_looking_for',
        'location': 'your_country',
        'current_salary': 'non_existent_salary'
    }

    bot = LinkedinAutomation(data)
    bot.login()
    bot.job_search()
    bot.apply()


