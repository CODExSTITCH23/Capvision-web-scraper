import sys
import os
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import sys
sys.path.append(os.path.dirname(__file__))
from slack_notify import notify_slack

JLT_URL = "https://www.bls.gov/jlt/latest-numbers.htm"
JLT_FOLDER = "scraped_data/jlt"
os.makedirs(JLT_FOLDER, exist_ok=True)

LABEL = "JOLTS Latest Numbers"

# Helper to get the latest file for deduplication/comparison
def get_latest_jlt_file():
    files = [f for f in os.listdir(JLT_FOLDER) if f.startswith(LABEL.replace(' ', '_'))]
    if not files:
        return None
    latest = sorted(files)[-1]
    with open(os.path.join(JLT_FOLDER, latest), 'r', encoding='utf-8') as f:
        return json.load(f)

def scrape_jlt_latest_numbers():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(JLT_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all spans with class "data-text"
        data_spans = soup.find_all("span", class_="data-text")
        
        if not data_spans:
            error = "No data spans with class 'data-text' found"
            print(error)
            notify_slack(f"❌ JOLTS Scraping Error: {error}")
            return {"error": error}
        
        all_data = []
        for span in data_spans:
            title = span.get('title', '')
            if not title:
                continue
                
            # Extract data value
            data_span = span.find("span", class_="data")
            data_value = data_span.get_text(strip=True) if data_span else ""
            
            # Extract period
            period_span = span.find("span", class_="period-text")
            period = period_span.get_text(strip=True) if period_span else ""
            
            # Extract year
            year_span = span.find("span", class_="year")
            year = year_span.get_text(strip=True) if year_span else ""
            
            # Combine the full text
            full_text = span.get_text(strip=True)
            
            all_data.append({
                "title": title,
                "data_value": data_value,
                "period": period,
                "year": year,
                "full_text": full_text
            })
        
        # Deduplication
        old = get_latest_jlt_file()
        old_data = old["data"] if old else None
        
        if not old or old_data != all_data:
            # Delete old files
            for file in os.listdir(JLT_FOLDER):
                if file.startswith(LABEL.replace(' ', '_')):
                    os.remove(os.path.join(JLT_FOLDER, file))
            filename = f"{JLT_FOLDER}/{LABEL.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "label": LABEL,
                    "timestamp": datetime.now().isoformat(),
                    "data": all_data
                }, f, indent=2)
            print(f"✅ Saved new JOLTS data at {filename}")
            
            # Send Slack notification for new data
            data_summary = f"📊 JOLTS Data Updated\n"
            data_summary += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            data_summary += f"📈 Found {len(all_data)} indicators\n"
            
            # Add top 5 indicators to notification
            for i, item in enumerate(all_data[:5]):
                data_summary += f"• {item['title']}: {item['data_value']} ({item['period']} {item['year']})\n"
            
            if len(all_data) > 5:
                data_summary += f"... and {len(all_data) - 5} more indicators"
            
            notify_slack(data_summary)
        else:
            print("No changes in JOLTS data.")
            notify_slack(f"JOLTS Data Check: No new data found at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("✅ JOLTS scraping completed.")
        return {"label": LABEL, "timestamp": datetime.now().isoformat(), "data": all_data}
    except Exception as e:
        error_msg = f"❌ Error in scrape_jlt_latest_numbers: {e}"
        print(error_msg)
        notify_slack(f"❌ JOLTS Scraping Error: {str(e)}")
        return {"error": str(e)}

def get_jlt_history():
    """
    Get the complete history of JOLTS data scrapes
    Returns a list of all scraped data files sorted by timestamp (newest first)
    """
    items = []
    try:
        for filename in sorted(os.listdir(JLT_FOLDER), reverse=True):
            if filename.endswith('.json') and filename.startswith(LABEL.replace(' ', '_')):
                with open(os.path.join(JLT_FOLDER, filename), 'r', encoding='utf-8') as f:
                    items.append(json.load(f))
    except Exception as e:
        print(f"Error reading JOLTS history: {e}")
    return items

def get_jlt_history_summary():
    """
    Get a summary of JOLTS scrape history
    Returns a dictionary with summary statistics
    """
    history = get_jlt_history()
    if not history:
        return {
            "total_scrapes": 0,
            "latest_scrape": None,
            "earliest_scrape": None,
            "total_indicators": 0,
            "average_indicators_per_scrape": 0
        }
    
    total_scrapes = len(history)
    latest_scrape = history[0]["timestamp"] if history else None
    earliest_scrape = history[-1]["timestamp"] if history else None
    
    total_indicators = sum(len(scrape["data"]) for scrape in history)
    avg_indicators = total_indicators / total_scrapes if total_scrapes > 0 else 0
    
    return {
        "total_scrapes": total_scrapes,
        "latest_scrape": latest_scrape,
        "earliest_scrape": earliest_scrape,
        "total_indicators": total_indicators,
        "average_indicators_per_scrape": round(avg_indicators, 2)
    }

# Keep the old function name for backward compatibility
def scrape_jlt_latest_number():
    return scrape_jlt_latest_numbers()

if __name__ == "__main__":
    result = scrape_jlt_latest_numbers()
    print(json.dumps(result, indent=2)) 