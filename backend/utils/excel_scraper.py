import requests
import pandas as pd
from io import BytesIO

EXCEL_URLS = {
    "Index of Consumer Sentiment": "https://data.sca.isr.umich.edu/get-table.php?c=YB&y=2025&m=2&n=1a&f=xls&k=ab66a79081fa0c8945717f7790e39b4c",
    "Components of the Index": "https://data.sca.isr.umich.edu/get-table.php?c=YB&y=2025&m=2&n=1b&f=xls&k=8987f5a4d8f30a4ad216ad2c3ac350c5",
    "Sentiment by Income Terciles": "https://data.sca.isr.umich.edu/get-table.php?c=YB&y=2025&m=2&n=2n&f=xls&k=6a297755fa716c1be4f2ee0b68197afa"
}

def fetch_excel_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_excel(BytesIO(response.content))
        return df.fillna("").to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

def get_all_sentiment_excel_data():
    results = {}
    for title, url in EXCEL_URLS.items():
        results[title] = fetch_excel_data(url)
    return results
