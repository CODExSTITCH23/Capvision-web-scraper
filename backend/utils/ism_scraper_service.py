import requests
from bs4 import BeautifulSoup

def scrape_ism_service():
    url = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/services/march/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the correct table
    table = soup.find("table", class_="mb-4")

    if not table:
        return {"error": "Service PMI table not found"}

    rows = table.find_all("tr")
    results = []

    # Define the expected column names
    column_names = [
        "Index",
        "Series Index Mar",
        "Series Index Feb",
        "Percentage Point Change",
        "Direction",
        "Rate of Change",
        "Trend (Months)"
    ]

    # Skip the header row
    for row in rows[1:]:
        cols = row.find_all(["td", "th"])
        if len(cols) >= 7:  # must have at least 7 columns
            item = {
                "Index": cols[0].text.strip(),
                "Series Index Mar": cols[1].text.strip(),
                "Series Index Feb": cols[2].text.strip(),
                "Percentage Point Change": cols[3].text.strip(),
                "Direction": cols[4].text.strip(),
                "Rate of Change": cols[5].text.strip(),
                "Trend (Months)": cols[6].text.strip(),
            }
            results.append(item)
        else:
            print(f"[WARNING] Skipping a row with only {len(cols)} columns")

    return results
