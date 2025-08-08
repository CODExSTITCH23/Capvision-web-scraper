from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Set up headless Chrome
options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load the page
url = "https://www.pmi.spglobal.com/"
driver.get(url)
time.sleep(5)  # Wait for dynamic content to load

# Get page source and parse it
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Find the ticker section (based on visual HTML)
ticker_section = soup.find_all("div", class_="carousel__cell")

# Extract PMI info
results = []
for item in ticker_section:
    country = item.find("div", class_="pmi-ticker__country")
    category = item.find("div", class_="pmi-ticker__sector")
    value = item.find("div", class_="pmi-ticker__value")
    label = item.find("div", class_="pmi-ticker__label")

    results.append({
        "country": country.text.strip() if country else None,
        "category": category.text.strip() if category else None,
        "value": value.text.strip() if value else None,
        "label": label.text.strip() if label else None
    })

# Print or process the results
for r in results:
    print(r)
