import requests
from bs4 import BeautifulSoup

def scrape_sentiment_data():
    url = "https://www.sca.isr.umich.edu/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    table = soup.find("table")
    rows = table.find_all("tr")
    results = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 6:
            results.append({
                "index": cols[0].text.strip(),
                "apr_2025": cols[1].text.strip(),
                "mar_2025": cols[2].text.strip(),
                "apr_2024": cols[3].text.strip(),
                "m_m": cols[4].text.strip(),
                "y_y": cols[5].text.strip(),
            })
    return results
