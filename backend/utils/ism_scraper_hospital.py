import requests
from bs4 import BeautifulSoup

def scrape_ism_hospital_pmi():
    url = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/hospital/march/"
    headers = {
        "User-Agent": "Mozilla/5.0"  # Always good to add User-Agent to avoid blocking
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the correct table
    table = soup.find("table", class_="table table-bordered table-hover")  # Look for class specifically

    if not table:
        return {"error": "Hospital PMI table not found"}

    rows = table.find_all("tr")
    results = []

    # Skip the header row
    for row in rows[1:]:
        cols = row.find_all(["td", "th"])
        if len(cols) >= 2:
            results.append({
                "month": cols[0].text.strip(),
                "Hospital PMI": cols[1].text.strip(),
            })

    return results
