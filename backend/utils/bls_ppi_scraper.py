import sys
import os
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
from utils.change_notify import compare_and_notify
from utils.slack_notify import notify_slack

BLS_PPI_URL = "https://www.bls.gov/ppi/latest-numbers.htm"
BLS_PPI_FOLDER = "scraped_data/bls_ppi"
os.makedirs(BLS_PPI_FOLDER, exist_ok=True)

TABLE_LABEL = "BLS PPI Latest Numbers"

# Helper to get the latest file for deduplication/comparison
def get_latest_bls_ppi_file():
    files = [f for f in os.listdir(BLS_PPI_FOLDER) if f.startswith(TABLE_LABEL.replace(' ', '_'))]
    if not files:
        return None
    latest = sorted(files)[-1]
    with open(os.path.join(BLS_PPI_FOLDER, latest), 'r', encoding='utf-8') as f:
        return json.load(f)

def scrape_bls_ppi_latest_numbers():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(BLS_PPI_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Find the group by class
        group = soup.find("div", class_="ln-group ln-group1 ppi")
        if not group:
            error = "PPI group not found"
            notify_slack(f"BLS PPI scraping failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {error}")
            return {"error": error}
        # Extract all tables within this group
        tables = group.find_all("table")
        all_tables = []
        for table in tables:
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            rows = []
            for tr in table.find_all("tr")[1:]:  # skip header
                cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if cols:
                    row = {headers[i]: cols[i] for i in range(min(len(headers), len(cols)))}
                    rows.append(row)
            all_tables.append({
                "headers": headers,
                "rows": rows
            })
        # Deduplication and change detection
        old = get_latest_bls_ppi_file()
        old_data = old["data"] if old else None
        changes_found = compare_and_notify(
            TABLE_LABEL,
            BLS_PPI_URL,
            old_data,
            all_tables,
            data_type="table"
        )
        # Save new data if changed
        if not old or old_data != all_tables:
            # Delete old files
            for file in os.listdir(BLS_PPI_FOLDER):
                if file.startswith(TABLE_LABEL.replace(' ', '_')):
                    os.remove(os.path.join(BLS_PPI_FOLDER, file))
            filename = f"{BLS_PPI_FOLDER}/{TABLE_LABEL.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "label": TABLE_LABEL,
                    "timestamp": datetime.now().isoformat(),
                    "data": all_tables
                }, f, indent=2)
            print(f"✅ Saved new BLS PPI data at {filename}")
        else:
            print("🟡 No changes in BLS PPI data.")
        if not changes_found:
            notify_slack(f"BLS PPI scraping completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No changes were found in this website.")
        print("✅ BLS PPI scraping completed.")
        return all_tables
    except Exception as e:
        print(f"❌ Error in scrape_bls_ppi_latest_numbers: {e}")
        notify_slack(f"BLS PPI scraping failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
        return {"error": str(e)}

def get_bls_ppi_history():
    items = []
    for filename in sorted(os.listdir(BLS_PPI_FOLDER), reverse=True):
        with open(os.path.join(BLS_PPI_FOLDER, filename), 'r', encoding='utf-8') as f:
            items.append(json.load(f))
    return items

if __name__ == "__main__":
    result = scrape_bls_ppi_latest_numbers()
    print(json.dumps(result, indent=2)) 