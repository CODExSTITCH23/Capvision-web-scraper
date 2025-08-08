import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
from utils.change_notify import compare_and_notify
from utils.slack_notify import notify_slack

BLS_URL = "https://www.bls.gov/news.release/cpi.htm"
BLS_FOLDER = "scraped_data/bls_cpi"
os.makedirs(BLS_FOLDER, exist_ok=True)

TABLE_LABEL = "BLS CPI Table A"

# Helper to get the latest file for deduplication/comparison
def get_latest_bls_file():
    files = [f for f in os.listdir(BLS_FOLDER) if f.startswith(TABLE_LABEL.replace(' ', '_'))]
    if not files:
        return None
    latest = sorted(files)[-1]
    with open(os.path.join(BLS_FOLDER, latest), 'r', encoding='utf-8') as f:
        return json.load(f)

def scrape_bls_cpi_table_a():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(BLS_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Find the table by its caption or summary
        table = None
        for t in soup.find_all("table"):
            caption = t.find("caption")
            if caption and "Percent changes in CPI for All Urban Consumers" in caption.text:
                table = t
                break
        if not table:
            error = "Table A not found"
            notify_slack(f"BLS CPI Table A scraping failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {error}")
            return {"error": error}
        # Parse the table
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        rows = []
        for tr in table.find_all("tr")[1:]:  # skip header
            cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            if cols:
                row = {headers[i]: cols[i] for i in range(min(len(headers), len(cols)))}
                rows.append(row)
        # Deduplication and change detection
        old = get_latest_bls_file()
        old_data = old["data"] if old else None
        changes_found = compare_and_notify(
            TABLE_LABEL,
            BLS_URL,
            old_data,
            rows,
            data_type="table"
        )
        # Save new data if changed
        if not old or old_data != rows:
            # Delete old files
            for file in os.listdir(BLS_FOLDER):
                if file.startswith(TABLE_LABEL.replace(' ', '_')):
                    os.remove(os.path.join(BLS_FOLDER, file))
            filename = f"{BLS_FOLDER}/{TABLE_LABEL.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "label": TABLE_LABEL,
                    "timestamp": datetime.now().isoformat(),
                    "data": rows
                }, f, indent=2)
            print(f"✅ Saved new BLS CPI Table A data at {filename}")
        else:
            print("🟡 No changes in BLS CPI Table A data.")
        if not changes_found:
            notify_slack(f"BLS CPI Table A scraping completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No changes were found in this website.")
        # notify_slack(f"BLS CPI Table A scraping completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("✅ BLS CPI Table A scraping completed.")
        return rows
    except Exception as e:
        print(f"❌ Error in scrape_bls_cpi_table_a: {e}")
        notify_slack(f"BLS CPI Table A scraping failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
        return {"error": str(e)}

def get_bls_cpi_history():
    items = []
    for filename in sorted(os.listdir(BLS_FOLDER), reverse=True):
        with open(os.path.join(BLS_FOLDER, filename), 'r', encoding='utf-8') as f:
            items.append(json.load(f))
    return items 