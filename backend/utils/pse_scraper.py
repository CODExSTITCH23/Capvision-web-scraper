import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
from utils.change_notify import compare_and_notify
from utils.slack_notify import notify_slack

PSE_URL = "https://edge.pse.com.ph/index/form.do"
PSE_FOLDER = "scraped_data/pse_index"
os.makedirs(PSE_FOLDER, exist_ok=True)

INDEX_LABEL = "PSE Index Summary"

INDEX_TABLE_CLASS = None  # The table does not have a class, so we'll find it by header

INDEX_KEYS = [
    "Index", "Value", "Chg", "%Chg"
]

# Helper to get the latest file for deduplication/comparison
def get_latest_pse_file():
    files = [f for f in os.listdir(PSE_FOLDER) if f.startswith(INDEX_LABEL.replace(' ', '_'))]
    if not files:
        return None
    latest = sorted(files)[-1]
    with open(os.path.join(PSE_FOLDER, latest), 'r', encoding='utf-8') as f:
        return json.load(f)

def scrape_pse_index():
    try:
        response = requests.get(PSE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Find the table by header text
        table = None
        for t in soup.find_all("table"):
            if t.find("th") and "Index" in t.find("th").text:
                table = t
                break
        if not table:
            error = "Index summary table not found"
            notify_slack(f"PSE Index scraping failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {error}")
            return {"error": error}
        rows = table.find_all("tr")[1:]  # skip header
        results = []
        for row in rows:
            cols = row.find_all(["td", "th"])
            if len(cols) >= 4:
                item = {k: cols[i].text.strip() for i, k in enumerate(INDEX_KEYS)}
                results.append(item)
        # Deduplication and change detection
        old = get_latest_pse_file()
        old_data = old["data"] if old else None
        changes_found = compare_and_notify(
            INDEX_LABEL,
            PSE_URL,
            old_data,
            results,
            data_type="table"
        )
        # Save new data if changed
        if not old or old_data != results:
            # Delete old files
            for file in os.listdir(PSE_FOLDER):
                if file.startswith(INDEX_LABEL.replace(' ', '_')):
                    os.remove(os.path.join(PSE_FOLDER, file))
            filename = f"{PSE_FOLDER}/{INDEX_LABEL.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "label": INDEX_LABEL,
                    "timestamp": datetime.now().isoformat(),
                    "data": results
                }, f, indent=2)
            print(f"✅ Saved new PSE index data at {filename}")
        else:
            print("🟡 No changes in PSE index data.")
        if not changes_found:
            notify_slack(f"PSE Index scraping completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No changes were found in this website.")
        # notify_slack(f"PSE Index scraping completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("✅ PSE Index scraping completed.")
        return results
    except Exception as e:
        print(f"❌ Error in scrape_pse_index: {e}")
        notify_slack(f"PSE Index scraping failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
        return {"error": str(e)}

def get_pse_index_history():
    items = []
    for filename in sorted(os.listdir(PSE_FOLDER), reverse=True):
        with open(os.path.join(PSE_FOLDER, filename), 'r', encoding='utf-8') as f:
            items.append(json.load(f))
    return items 