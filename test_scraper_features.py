#!/usr/bin/env python3
"""
Test script to demonstrate the new scrape history and Slack notification features
for both JLT and Conference Board scrapers.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'utils'))

from jlt_scraper import get_jlt_history_summary, get_jlt_history
from conference_board_scraper import get_conference_board_history_summary, get_conference_board_history

def test_scraper_features():
    print("🧪 Testing Scraper Features")
    print("=" * 50)
    
    # Test JLT History
    print("\n📊 JOLTS Scrape History Summary:")
    jlt_summary = get_jlt_history_summary()
    print(f"Total scrapes: {jlt_summary['total_scrapes']}")
    print(f"Latest scrape: {jlt_summary['latest_scrape']}")
    print(f"Earliest scrape: {jlt_summary['earliest_scrape']}")
    print(f"Total indicators: {jlt_summary['total_indicators']}")
    print(f"Average indicators per scrape: {jlt_summary['average_indicators_per_scrape']}")
    
    # Test Conference Board History
    print("\n📊 Conference Board Scrape History Summary:")
    cb_summary = get_conference_board_history_summary()
    print(f"Total scrapes: {cb_summary['total_scrapes']}")
    print(f"Latest scrape: {cb_summary['latest_scrape']}")
    print(f"Earliest scrape: {cb_summary['earliest_scrape']}")
    print(f"Total indicators: {cb_summary['total_indicators']}")
    print(f"Average indicators per scrape: {cb_summary['average_indicators_per_scrape']}")
    
    # Show indicator types for Conference Board
    if cb_summary['indicator_types']:
        print("\nIndicator types found:")
        for ind_type, count in cb_summary['indicator_types'].items():
            print(f"  • {ind_type}: {count} occurrences")
    
    # Test getting full history
    print("\n📋 Latest JOLTS Data:")
    jlt_history = get_jlt_history()
    if jlt_history:
        latest_jlt = jlt_history[0]
        print(f"Timestamp: {latest_jlt['timestamp']}")
        print(f"Indicators found: {len(latest_jlt['data'])}")
        for i, item in enumerate(latest_jlt['data'][:3]):  # Show first 3
            print(f"  {i+1}. {item['title']}: {item['data_value']}")
    
    print("\n📋 Latest Conference Board Data:")
    cb_history = get_conference_board_history()
    if cb_history:
        latest_cb = cb_history[0]
        print(f"Timestamp: {latest_cb['timestamp']}")
        print(f"Indicators found: {len(latest_cb['data'])}")
        for i, item in enumerate(latest_cb['data'][:3]):  # Show first 3
            region = item.get('region', 'Unknown')
            percentage = item.get('percentage', 'N/A')
            indicator = item.get('indicator', 'Unknown')
            print(f"  {i+1}. {region}: {percentage} ({indicator})")
    
    print("\n✅ Feature test completed!")

if __name__ == "__main__":
    test_scraper_features() 