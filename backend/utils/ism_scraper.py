import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
import hashlib
from utils.slack_notify import notify_slack
from utils.change_notify import compare_and_notify

HEADERS = {"User-Agent": "Mozilla/5.0"}
ISM_FOLDER = "scraped_data/ism_data"
os.makedirs(ISM_FOLDER, exist_ok=True)

def content_hash(content):
    return hashlib.md5(json.dumps(content, sort_keys=True).encode('utf-8')).hexdigest()

def save_ism_data(label, data):
    try:
        if not isinstance(data, list) or not data:
            print(f"⚠️ No data to save for {label}")
            return
        # Compute hash to prevent duplicates
        new_hash = content_hash(data)
        label_prefix = label.replace(" ", "_")
        old_data = None
        url = None
        # Set the URL for Manufacturing PMI
        if label == "Manufacturing PMI":
            url = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/"
        for file in os.listdir(ISM_FOLDER):
            if file.startswith(label_prefix):
                with open(os.path.join(ISM_FOLDER, file), 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    old_data = existing["data"]
                    if content_hash(existing["data"]) == new_hash:
                        print(f"🟡 Skipping duplicate: {label}")
                        return
        # Compare and notify for Manufacturing PMI only
        if label == "Manufacturing PMI" and old_data is not None and url:
            compare_and_notify(label, url, old_data, data, data_type="table")
        # If here, content is new: delete all old files for this label
        for file in os.listdir(ISM_FOLDER):
            if file.startswith(label_prefix):
                os.remove(os.path.join(ISM_FOLDER, file))
        filename = f"{ISM_FOLDER}/{label_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "label": label,
                "timestamp": datetime.now().isoformat(),
                "data": data
            }, f, indent=2)
        print(f"✅ Saved new ISM data for {label} at {filename}")
    except Exception as e:
        print(f"❌ Error in save_ism_data for {label}: {e}")

def scrape_hospital_pmi():
    url = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/hospital/june/"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="table table-bordered table-hover")
    if not table:
        return {"error": "Hospital PMI table not found"}

    results = []
    for row in table.find_all("tr")[1:]:
        cols = row.find_all(["td", "th"])
        if len(cols) >= 2:
            results.append({
                "month": cols[0].text.strip(),
                "Hospital PMI": cols[1].text.strip()
            })

    save_ism_data("Hospital PMI", results)
    return results

def scrape_service_pmi():
    url = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/services/june/"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="mb-4")
    if not table:
        return {"error": "Service PMI table not found"}

    results = []
    for row in table.find_all("tr")[1:]:
        cols = row.find_all(["td", "th"])
        if len(cols) >= 7:
            results.append({
                "Index": cols[0].text.strip(),
                "Series Index Mar": cols[1].text.strip(),
                "Series Index Feb": cols[2].text.strip(),
                "Percentage Point Change": cols[3].text.strip(),
                "Direction": cols[4].text.strip(),
                "Rate of Change": cols[5].text.strip(),
                "Trend (Months)": cols[6].text.strip(),
            })

    save_ism_data("Service PMI", results)
    return results

def scrape_manufacturing_pmi():
    url = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/pmi/june/"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="mb-4")
    if not table:
        return {"error": "Manufacturing PMI table not found"}

    results = []
    for row in table.find_all("tr")[1:]:
        cols = row.find_all(["td", "th"])
        if len(cols) >= 7:
            results.append({
                "Index": cols[0].text.strip(),
                "Series Index Mar": cols[1].text.strip(),
                "Series Index Feb": cols[2].text.strip(),
                "Percentage Point Change": cols[3].text.strip(),
                "Direction": cols[4].text.strip(),
                "Rate of Change": cols[5].text.strip(),
                "Trend (Months)": cols[6].text.strip(),
            })

    save_ism_data("Manufacturing PMI", results)
    return results

def get_all_ism_data():
    try:
        changes_found = False
        # Hospital PMI
        hospital_label = "Hospital PMI"
        hospital_url = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/hospital/june/"
        hospital_old = None
        hospital_prefix = hospital_label.replace(" ", "_")
        for file in os.listdir(ISM_FOLDER):
            if file.startswith(hospital_prefix):
                with open(os.path.join(ISM_FOLDER, file), 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    hospital_old = existing["data"]
                    break
        hospital_new = scrape_hospital_pmi()
        if compare_and_notify(hospital_label, hospital_url, hospital_old, hospital_new, data_type="table"):
            changes_found = True
        # Service PMI
        service_label = "Service PMI"
        service_url = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/services/june/"
        service_old = None
        service_prefix = service_label.replace(" ", "_")
        for file in os.listdir(ISM_FOLDER):
            if file.startswith(service_prefix):
                with open(os.path.join(ISM_FOLDER, file), 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    service_old = existing["data"]
                    break
        service_new = scrape_service_pmi()
        if compare_and_notify(service_label, service_url, service_old, service_new, data_type="table"):
            changes_found = True
        # Manufacturing PMI
        manuf_label = "Manufacturing PMI"
        manuf_url = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/"
        manuf_old = None
        manuf_prefix = manuf_label.replace(" ", "_")
        for file in os.listdir(ISM_FOLDER):
            if file.startswith(manuf_prefix):
                with open(os.path.join(ISM_FOLDER, file), 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    manuf_old = existing["data"]
                    break
        manuf_new = scrape_manufacturing_pmi()
        if compare_and_notify(manuf_label, manuf_url, manuf_old, manuf_new, data_type="table"):
            changes_found = True
        result = {
            hospital_label: hospital_new,
            service_label: service_new,
            manuf_label: manuf_new
        }
        if not changes_found:
            notify_slack("No changes were found in this website.")
        notify_slack(f"ISM scraping completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("✅ ISM scraping completed.")
        return result
    except Exception as e:
        print(f"❌ Error in get_all_ism_data: {e}")
        notify_slack(f"ISM scraping failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
        return {"error": str(e)}

def get_ism_history():
    history = []
    for filename in sorted(os.listdir(ISM_FOLDER), reverse=True):
        filepath = os.path.join(ISM_FOLDER, filename)
        if filename.endswith(".json"):
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    history.append(json.load(f))
                except Exception as e:
                    print(f"⚠️ Failed to load {filename}: {e}")
    return history

def main():
    print("Choose an option:")
    print("1. Scrape Hospital PMI")
    print("2. Scrape Service PMI")
    print("3. Scrape Manufacturing PMI")

    choice = input("Enter your choice (1–3): ").strip()

    if choice == "1":
        print("\nScraping Hospital PMI...\n")
        print(scrape_hospital_pmi())
    elif choice == "2":
        print("\nScraping Service PMI...\n")
        print(scrape_service_pmi())
    elif choice == "3":
        print("\nScraping Manufacturing PMI...\n")
        print(scrape_manufacturing_pmi())
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
