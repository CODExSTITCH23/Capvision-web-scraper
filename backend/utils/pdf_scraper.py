import requests
import pdfplumber
from io import BytesIO
import os
import json
from datetime import datetime
import hashlib  # added for content hashing
from utils.slack_notify import notify_slack
from utils.change_notify import compare_and_notify

PDF_URLS = {
    "Index of Consumer Sentiment": "https://www.sca.isr.umich.edu/files/tbcics.pdf",
    "Components of the Index": "https://www.sca.isr.umich.edu/files/tbciccice.pdf",
    "Sentiment by Income Terciles": "https://www.sca.isr.umich.edu/files/tbcpx1px5.pdf"
}

PDF_FOLDER = "scraped_data/pdf_sentiments"
os.makedirs(PDF_FOLDER, exist_ok=True)

def extract_pdf_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with pdfplumber.open(BytesIO(response.content)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        return {"error": str(e)}

# 🔒 New: hash utility
def content_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

# 🧠 Updated: deduplicated saving
def save_pdf_data(title, content):
    try:
        new_hash = content_hash(content)
        title_prefix = title.replace(" ", "_")
        duplicate_found = False
        for file in os.listdir(PDF_FOLDER):
            if file.startswith(title_prefix):
                with open(os.path.join(PDF_FOLDER, file), 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    if content_hash(existing["content"]) == new_hash:
                        print(f"🟡 Skipping duplicate: {title}")
                        return  # Don't save duplicate
        # If here, content is new: delete all old files for this title
        for file in os.listdir(PDF_FOLDER):
            if file.startswith(title_prefix):
                os.remove(os.path.join(PDF_FOLDER, file))
        filename = f"{PDF_FOLDER}/{title_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "title": title,
                "timestamp": datetime.now().isoformat(),
                "content": content
            }, f, indent=2)
        print(f"✅ Saved new PDF data for {title} at {filename}")
    except Exception as e:
        print(f"❌ Error in save_pdf_data for {title}: {e}")

def get_all_sentiment_pdf_data():
    try:
        results = {}
        changes_found = False
        for title, url in PDF_URLS.items():
            print(f"🔎 Scraping PDF: {title} from {url}")
            content = extract_pdf_text(url)
            results[title] = content
            # Load previous content for comparison
            old_content = None
            title_prefix = title.replace(" ", "_")
            for file in os.listdir(PDF_FOLDER):
                if file.startswith(title_prefix):
                    with open(os.path.join(PDF_FOLDER, file), 'r', encoding='utf-8') as f:
                        existing = json.load(f)
                        old_content = existing["content"]
                        break
            if compare_and_notify(title, url, old_content, content, data_type="text"):
                changes_found = True
            save_pdf_data(title, content)
        if not changes_found:
            notify_slack(f"PDF Sentiment scraping completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No changes were found in this website.")
        # notify_slack(f"PDF Sentiment scraping completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("✅ PDF Sentiment scraping completed.")
        return results
    except Exception as e:
        print(f"❌ Error in get_all_sentiment_pdf_data: {e}")
        notify_slack(f"PDF Sentiment scraping failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
        return {"error": str(e)}

def get_pdf_sentiment_history():
    items = []
    for filename in sorted(os.listdir(PDF_FOLDER), reverse=True):
        with open(os.path.join(PDF_FOLDER, filename), 'r', encoding='utf-8') as f:
            items.append(json.load(f))
    return items
