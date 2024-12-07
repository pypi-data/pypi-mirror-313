import csv
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_sanskrit(query):
    # Construct the URL
    base_url = "https://sanskritdictionary.com/"
    params = {
        "iencoding": "hk",
        "q": query,
        "lang": "sans",
        "action": "Search"
    }
    search_url = f"{base_url}?{urllib.parse.urlencode(params)}"

    # Set up Selenium
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Open the search URL
        driver.get(search_url)

        # Wait for the desired content to load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "thinborder.monierWilliamsTblRes"))
        )
        html = driver.page_source

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        result_div = soup.find("div", class_="thinborder monierWilliamsTblRes")

        if result_div:
            # Extract rows
            rows = result_div.find_all("tr")
            data = []
            for row in rows:
                if 'background: LightYellow' in str(row.get('style', '')):
                    columns = row.find_all("td")
                    if columns:
                        row_data = [col.text.strip() for col in columns]
                        data.append(row_data)

            # Save to CSV
            csv_filename = f"{query}_data.csv"
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([header.text.strip() for header in result_div.find_all("th")])
                writer.writerows(data)

            print(f"Filtered data has been saved to '{csv_filename}'.")
            return data
        else:
            print("No results found.")
            return None
    finally:
        driver.quit()

def main():
    query = input("Enter your query: ")
    scrape_sanskrit(query)
