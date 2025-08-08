import sys
import os
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re
import time
import sys
sys.path.append(os.path.dirname(__file__))
from slack_notify import notify_slack

CONFERENCE_BOARD_URL = "https://www.conference-board.org/topics/consumer-confidence/"
CONFERENCE_BOARD_FOLDER = "scraped_data/conference_board"
os.makedirs(CONFERENCE_BOARD_FOLDER, exist_ok=True)

LABEL = "Conference Board Economic Indicators"

# Helper to get the latest file for deduplication/comparison
def get_latest_conference_board_file():
    files = [f for f in os.listdir(CONFERENCE_BOARD_FOLDER) if f.startswith(LABEL.replace(' ', '_'))]
    if not files:
        return None
    latest = sorted(files)[-1]
    with open(os.path.join(CONFERENCE_BOARD_FOLDER, latest), 'r', encoding='utf-8') as f:
        return json.load(f)

def scrape_conference_board_indicators():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        session = requests.Session()
        response = session.get(CONFERENCE_BOARD_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        print(f"Page title: {soup.title.string if soup.title else 'No title found'}")
        
        # Always save debug HTML for analysis
        debug_filename = f"{CONFERENCE_BOARD_FOLDER}/debug_page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(debug_filename, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"Saved debug HTML to {debug_filename}")
        
        all_indicators = []
        
        # Approach 1: Look for all carousel sections
        print("Looking for all carousel sections...")
        
        # Find all carousel containers
        carousel_containers = soup.find_all("div", class_="owl-carousel")
        print(f"Found {len(carousel_containers)} carousel containers")
        
        for i, carousel in enumerate(carousel_containers):
            print(f"Processing carousel {i+1}")
            
            # Look for owl-item elements within this carousel
            owl_items = carousel.find_all("div", class_="owl-item")
            print(f"  Found {len(owl_items)} owl-item elements in carousel {i+1}")
            
            for owl_item in owl_items:
                # Look for item class within owl-item
                item = owl_item.find("div", class_="item")
                if not item:
                    continue
                    
                # Look for down class within item
                down = item.find("div", class_="down")
                if not down:
                    continue
                    
                # Look for anchor tag within down
                anchor = down.find("a")
                if not anchor:
                    continue
                    
                # Extract the text content
                text_content = anchor.get_text(strip=True)
                href = anchor.get('href', '')
                
                # Parse the text content to extract components
                if text_content:
                    match = re.match(r'([+-]?\s*[\d.]+%)\s+(.+?)\s+([A-Z]+)$', text_content)
                    if match:
                        percentage = match.group(1).strip()
                        region = match.group(2).strip()
                        indicator = match.group(3).strip()
                        
                        all_indicators.append({
                            "percentage": percentage,
                            "region": region,
                            "indicator": indicator,
                            "full_text": text_content,
                            "href": href,
                            "carousel_index": i+1
                        })
                    else:
                        all_indicators.append({
                            "percentage": "",
                            "region": "",
                            "indicator": "",
                            "full_text": text_content,
                            "href": href,
                            "carousel_index": i+1
                        })
        
        # Approach 2: Look for any elements with "down" class across the entire page
        if not all_indicators:
            print("Trying alternative approach: looking for 'down' class elements")
            down_elements = soup.find_all("div", class_="down")
            print(f"Found {len(down_elements)} down elements")
            
            for down in down_elements:
                anchor = down.find("a")
                if anchor:
                    text_content = anchor.get_text(strip=True)
                    href = anchor.get('href', '')
                    
                    if text_content and any(char.isdigit() for char in text_content):
                        match = re.match(r'([+-]?\s*[\d.]+%)\s+(.+?)\s+([A-Z]+)$', text_content)
                        if match:
                            percentage = match.group(1).strip()
                            region = match.group(2).strip()
                            indicator = match.group(3).strip()
                            
                            all_indicators.append({
                                "percentage": percentage,
                                "region": region,
                                "indicator": indicator,
                                "full_text": text_content,
                                "href": href
                            })
        
        # Approach 3: Look for any links that contain percentage data and indicator patterns
        if not all_indicators:
            print("Trying third approach: looking for links with percentage data")
            all_links = soup.find_all("a", href=True)
            print(f"Found {len(all_links)} total links")
            
            for link in all_links:
                text_content = link.get_text(strip=True)
                href = link.get('href', '')
                
                if text_content and '%' in text_content:
                    # Try multiple regex patterns to match different formats
                    patterns = [
                        r'([+-]?\s*[\d.]+%)\s+(.+?)\s+([A-Z]+)$',  # Standard format
                        r'([+-]?\s*[\d.]+%)\s+([A-Z]+)\s+(.+?)$',  # Reversed format
                        r'([A-Z]+)\s+([+-]?\s*[\d.]+%)\s+(.+?)$',  # Indicator first
                    ]
                    
                    for pattern in patterns:
                        match = re.match(pattern, text_content)
                        if match:
                            if pattern == patterns[0]:  # Standard format
                                percentage = match.group(1).strip()
                                region = match.group(2).strip()
                                indicator = match.group(3).strip()
                            elif pattern == patterns[1]:  # Reversed format
                                percentage = match.group(1).strip()
                                indicator = match.group(2).strip()
                                region = match.group(3).strip()
                            else:  # Indicator first
                                indicator = match.group(1).strip()
                                percentage = match.group(2).strip()
                                region = match.group(3).strip()
                            
                            all_indicators.append({
                                "percentage": percentage,
                                "region": region,
                                "indicator": indicator,
                                "full_text": text_content,
                                "href": href
                            })
                            break
        
        # Approach 4: Look for specific sections by their IDs or classes
        print("Trying approach 4: looking for specific sections")
        
        # Look for sections that might contain different types of indicators
        sections = soup.find_all(["section", "div"], class_=re.compile(r'(indicator|economic|confidence|leading)', re.I))
        print(f"Found {len(sections)} potential indicator sections")
        
        for section in sections:
            # Look for links within each section
            links = section.find_all("a", href=True)
            for link in links:
                text_content = link.get_text(strip=True)
                href = link.get('href', '')
                
                if text_content and '%' in text_content:
                    # Try to parse the content
                    patterns = [
                        r'([+-]?\s*[\d.]+%)\s+(.+?)\s+([A-Z]+)$',
                        r'([+-]?\s*[\d.]+%)\s+([A-Z]+)\s+(.+?)$',
                        r'([A-Z]+)\s+([+-]?\s*[\d.]+%)\s+(.+?)$',
                    ]
                    
                    for pattern in patterns:
                        match = re.match(pattern, text_content)
                        if match:
                            if pattern == patterns[0]:
                                percentage = match.group(1).strip()
                                region = match.group(2).strip()
                                indicator = match.group(3).strip()
                            elif pattern == patterns[1]:
                                percentage = match.group(1).strip()
                                indicator = match.group(2).strip()
                                region = match.group(3).strip()
                            else:
                                indicator = match.group(1).strip()
                                percentage = match.group(2).strip()
                                region = match.group(3).strip()
                            
                            # Check if this indicator is already captured
                            duplicate = False
                            for existing in all_indicators:
                                if (existing.get('percentage') == percentage and 
                                    existing.get('region') == region and 
                                    existing.get('indicator') == indicator):
                                    duplicate = True
                                    break
                            
                            if not duplicate:
                                all_indicators.append({
                                    "percentage": percentage,
                                    "region": region,
                                    "indicator": indicator,
                                    "full_text": text_content,
                                    "href": href
                                })
                            break
        
        # Approach 5: Look for any text content that matches indicator patterns
        print("Trying approach 5: looking for any text with percentage patterns")
        
        # Find all text nodes that contain percentage data
        for element in soup.find_all(string=True):
            text_content = element.strip()
            if text_content and '%' in text_content and any(char.isdigit() for char in text_content):
                # Look for patterns in the text
                patterns = [
                    r'([+-]?\s*[\d.]+%)\s+(.+?)\s+([A-Z]+)$',
                    r'([+-]?\s*[\d.]+%)\s+([A-Z]+)\s+(.+?)$',
                    r'([A-Z]+)\s+([+-]?\s*[\d.]+%)\s+(.+?)$',
                ]
                
                for pattern in patterns:
                    match = re.match(pattern, text_content)
                    if match:
                        if pattern == patterns[0]:
                            percentage = match.group(1).strip()
                            region = match.group(2).strip()
                            indicator = match.group(3).strip()
                        elif pattern == patterns[1]:
                            percentage = match.group(1).strip()
                            indicator = match.group(2).strip()
                            region = match.group(3).strip()
                        else:
                            indicator = match.group(1).strip()
                            percentage = match.group(2).strip()
                            region = match.group(3).strip()
                        
                        # Check if this indicator is already captured
                        duplicate = False
                        for existing in all_indicators:
                            if (existing.get('percentage') == percentage and 
                                existing.get('region') == region and 
                                existing.get('indicator') == indicator):
                                duplicate = True
                                break
                        
                        if not duplicate:
                            all_indicators.append({
                                "percentage": percentage,
                                "region": region,
                                "indicator": indicator,
                                "full_text": text_content,
                                "href": ""
                            })
                        break
        
        # Approach 6: Look for links with business-cycle-indicators pattern
        print("Trying approach 6: looking for business-cycle-indicators links")
        
        # Find all links that contain business-cycle-indicators
        business_cycle_links = soup.find_all("a", href=re.compile(r'/topics/business-cycle-indicators'))
        print(f"Found {len(business_cycle_links)} business-cycle-indicators links")
        
        for link in business_cycle_links:
            text_content = link.get_text(strip=True)
            href = link.get('href', '')
            
            if text_content and '%' in text_content:
                # Try to parse the content
                patterns = [
                    r'([+-]?\s*[\d.]+%)\s+(.+?)\s+([A-Z]+)$',
                    r'([+-]?\s*[\d.]+%)\s+([A-Z]+)\s+(.+?)$',
                    r'([A-Z]+)\s+([+-]?\s*[\d.]+%)\s+(.+?)$',
                ]
                
                for pattern in patterns:
                    match = re.match(pattern, text_content)
                    if match:
                        if pattern == patterns[0]:
                            percentage = match.group(1).strip()
                            region = match.group(2).strip()
                            indicator = match.group(3).strip()
                        elif pattern == patterns[1]:
                            percentage = match.group(1).strip()
                            indicator = match.group(2).strip()
                            region = match.group(3).strip()
                        else:
                            indicator = match.group(1).strip()
                            percentage = match.group(2).strip()
                            region = match.group(3).strip()
                        
                        # Check if this indicator is already captured
                        duplicate = False
                        for existing in all_indicators:
                            if (existing.get('percentage') == percentage and 
                                existing.get('region') == region and 
                                existing.get('indicator') == indicator):
                                duplicate = True
                                break
                        
                        if not duplicate:
                            all_indicators.append({
                                "percentage": percentage,
                                "region": region,
                                "indicator": indicator,
                                "full_text": text_content,
                                "href": href
                            })
                        break
        
        # Approach 7: Look for the actual text content that contains the indicators
        print("Trying approach 7: looking for raw text content with indicators")
        
        # Find all text content that contains percentage and region patterns
        all_text = soup.get_text()
        lines = all_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and '%' in line and any(char.isdigit() for char in line):
                # Look for patterns in the text
                patterns = [
                    r'([+-]?\s*[\d.]+%)\s+(.+?)\s+([A-Z]+)$',  # Standard format: percentage region indicator
                    r'([+-]?\s*[\d.]+%)\s+([A-Z]+)\s+(.+?)$',  # Reversed format: percentage indicator region
                    r'([A-Z]+)\s+([+-]?\s*[\d.]+%)\s+(.+?)$',  # Indicator first: indicator percentage region
                    r'([+-]?\s*[\d.]+%)\s+([A-Z]+)$',          # No region: percentage indicator
                    r'([A-Z]+)\s+([+-]?\s*[\d.]+%)$',          # Indicator first, no region: indicator percentage
                ]
                
                for pattern in patterns:
                    match = re.match(pattern, line)
                    if match:
                        if pattern == patterns[0]:  # Standard format
                            percentage = match.group(1).strip()
                            region = match.group(2).strip()
                            indicator = match.group(3).strip()
                        elif pattern == patterns[1]:  # Reversed format
                            percentage = match.group(1).strip()
                            indicator = match.group(2).strip()
                            region = match.group(3).strip()
                        elif pattern == patterns[2]:  # Indicator first
                            indicator = match.group(1).strip()
                            percentage = match.group(2).strip()
                            region = match.group(3).strip()
                        elif pattern == patterns[3]:  # No region
                            percentage = match.group(1).strip()
                            indicator = match.group(2).strip()
                            region = ""
                        elif pattern == patterns[4]:  # Indicator first, no region
                            indicator = match.group(1).strip()
                            percentage = match.group(2).strip()
                            region = ""
                        
                        # Check if this indicator is already captured
                        duplicate = False
                        for existing in all_indicators:
                            if (existing.get('percentage') == percentage and 
                                existing.get('region') == region and 
                                existing.get('indicator') == indicator):
                                duplicate = True
                                break
                        
                        if not duplicate:
                            all_indicators.append({
                                "percentage": percentage,
                                "region": region,
                                "indicator": indicator,
                                "full_text": line,
                                "href": ""
                            })
                        break
        
        if not all_indicators:
            error = "No indicator data found using any approach"
            print(error)
            notify_slack(f"❌ Conference Board Scraping Error: {error}")
            return {"error": error}
        
        print(f"Found {len(all_indicators)} indicators")
        
        # Remove duplicates based on percentage, region, and indicator
        unique_indicators = []
        seen = set()
        for indicator in all_indicators:
            key = (indicator.get('percentage', ''), indicator.get('region', ''), indicator.get('indicator', ''))
            if key not in seen:
                seen.add(key)
                unique_indicators.append(indicator)
        
        print(f"After deduplication: {len(unique_indicators)} unique indicators")
        
        # Deduplication
        old = get_latest_conference_board_file()
        old_data = old["data"] if old else None
        
        if not old or old_data != unique_indicators:
            # Delete old files (but keep debug files)
            for file in os.listdir(CONFERENCE_BOARD_FOLDER):
                if file.startswith(LABEL.replace(' ', '_')):
                    os.remove(os.path.join(CONFERENCE_BOARD_FOLDER, file))
            filename = f"{CONFERENCE_BOARD_FOLDER}/{LABEL.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "label": LABEL,
                    "timestamp": datetime.now().isoformat(),
                    "data": unique_indicators
                }, f, indent=2)
            print(f"✅ Saved new Conference Board data at {filename}")
            
            # # Send Slack notification for new data
            # data_summary = f"📊 Conference Board Data Updated\n"
            # data_summary += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            # data_summary += f"📈 Found {len(unique_indicators)} indicators\n"
            
            # # Group indicators by type
            # indicators_by_type = {}
            # for indicator in unique_indicators:
            #     ind_type = indicator.get('indicator', 'Unknown')
            #     if ind_type not in indicators_by_type:
            #         indicators_by_type[ind_type] = []
            #     indicators_by_type[ind_type].append(indicator)
            
            # # Add summary by indicator type
            # for ind_type, indicators in indicators_by_type.items():
            #     data_summary += f"• {ind_type}: {len(indicators)} indicators\n"
            
            # # Add top 5 indicators to notification
            # data_summary += f"\nTop indicators:\n"
            # for i, indicator in enumerate(unique_indicators[:5]):
            #     region = indicator.get('region', 'Unknown')
            #     percentage = indicator.get('percentage', 'N/A')
            #     ind_type = indicator.get('indicator', 'Unknown')
            #     data_summary += f"• {region}: {percentage} ({ind_type})\n"
            
            # if len(unique_indicators) > 5:
            #     data_summary += f"... and {len(unique_indicators) - 5} more indicators"
            
            # notify_slack(data_summary)
        else:
            print("No changes in Conference Board data.")
            notify_slack(f"Conference Board Data Check: No new data found at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("✅ Conference Board scraping completed.")
        return {"label": LABEL, "timestamp": datetime.now().isoformat(), "data": unique_indicators}
    except Exception as e:
        error_msg = f"❌ Error in scrape_conference_board_indicators: {e}"
        print(error_msg)
        notify_slack(f"❌ Conference Board Scraping Error: {str(e)}")
        return {"error": str(e)}

def get_conference_board_history():
    """
    Get the complete history of Conference Board data scrapes
    Returns a list of all scraped data files sorted by timestamp (newest first)
    """
    items = []
    try:
        for filename in sorted(os.listdir(CONFERENCE_BOARD_FOLDER), reverse=True):
            if filename.endswith('.json') and filename.startswith(LABEL.replace(' ', '_')):
                with open(os.path.join(CONFERENCE_BOARD_FOLDER, filename), 'r', encoding='utf-8') as f:
                    items.append(json.load(f))
    except Exception as e:
        print(f"Error reading Conference Board history: {e}")
    return items

def get_conference_board_history_summary():
    """
    Get a summary of Conference Board scrape history
    Returns a dictionary with summary statistics
    """
    history = get_conference_board_history()
    if not history:
        return {
            "total_scrapes": 0,
            "latest_scrape": None,
            "earliest_scrape": None,
            "total_indicators": 0,
            "average_indicators_per_scrape": 0,
            "indicator_types": {}
        }
    
    total_scrapes = len(history)
    latest_scrape = history[0]["timestamp"] if history else None
    earliest_scrape = history[-1]["timestamp"] if history else None
    
    total_indicators = sum(len(scrape["data"]) for scrape in history)
    avg_indicators = total_indicators / total_scrapes if total_scrapes > 0 else 0
    
    # Count indicator types
    indicator_types = {}
    for scrape in history:
        for indicator in scrape["data"]:
            ind_type = indicator.get('indicator', 'Unknown')
            indicator_types[ind_type] = indicator_types.get(ind_type, 0) + 1
    
    return {
        "total_scrapes": total_scrapes,
        "latest_scrape": latest_scrape,
        "earliest_scrape": earliest_scrape,
        "total_indicators": total_indicators,
        "average_indicators_per_scrape": round(avg_indicators, 2),
        "indicator_types": indicator_types
    }

if __name__ == "__main__":
    result = scrape_conference_board_indicators()
    print(json.dumps(result, indent=2)) 