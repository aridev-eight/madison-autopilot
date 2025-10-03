#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pytrends.request import TrendReq
import time

def collect_trends_data():
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    pytrends = TrendReq(hl='en-US', tz=360)
    keywords = ['Google', 'Google Pixel', 'Android', 'Gmail', 'Google Chrome']
    
    all_trends = []
    
    for keyword in keywords:
        try:
            print(f"Collecting trends for: {keyword}")
            pytrends.build_payload([keyword], timeframe='today 3-m')
            interest_over_time = pytrends.interest_over_time()
            
            if not interest_over_time.empty:
                trends_data = {
                    'keyword': keyword,
                    'average_interest': float(interest_over_time[keyword].mean()),
                    'max_interest': int(interest_over_time[keyword].max()),
                    'recent_trend': 'rising' if interest_over_time[keyword].iloc[-1] > interest_over_time[keyword].mean() else 'stable'
                }
                all_trends.append(trends_data)
            
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"Error for {keyword}: {str(e)}")
            continue
    
    output = {
        'source': 'google_trends',
        'timestamp': datetime.now().isoformat(),
        'keywords_searched': keywords,
        'trends': all_trends
    }
    
    # Save with consistent filename for n8n to find
    output_file = os.path.join(script_dir, 'google_trends_latest.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved to: {output_file}")
    print(f"Collected: {len(all_trends)} keywords")
    
    return output_file

if __name__ == "__main__":
    collect_trends_data()
