# import requests
# from bs4 import BeautifulSoup

# def scrape_pmi_marquee():
#     url = "https://www.pmi.spglobal.com/"
#     headers = {"User-Agent": "Mozilla/5.0"}

#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, "html.parser")

#     data = []
#     items = soup.select("div.indexItem")

#     for item in items:
#         country = item.select_one(".indexName")
#         pmi_type = item.select_one(".instrumentTypeDescription")
#         value = item.select_one(".indexFigure")
#         comment = item.select_one(".indexComment")

#         data.append({
#             "country": country.text.strip() if country else "",
#             "type": pmi_type.text.strip() if pmi_type else "",
#             "value": value.text.strip() if value else "",
#             "comment": comment.text.strip() if comment else "",
#         })

#     return data

import requests
from bs4 import BeautifulSoup

def scrape_pmi_marquee():
    try:
        # Make a GET request to the page
        print("Navigating to page...")
        response = requests.get("https://www.pmi.spglobal.com/")
        response.raise_for_status()  # Raise an exception for HTTP errors

        print("Parsing page...")
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")

        print("Extracting elements...")
        # Find all elements containing the desired data
        items = soup.find_all("div", class_="indexItem")
        data = []

        for item in items:
            country = item.find(class_="indexName")
            pmi_type = item.find(class_="instrumentTypeDescription")
            value = item.find(class_="indexFigure")
            comment = item.find(class_="indexComment")

            data.append({
                "country": country.get_text(strip=True) if country else "",
                "type": pmi_type.get_text(strip=True) if pmi_type else "",
                "value": value.get_text(strip=True) if value else "",
                "comment": comment.get_text(strip=True) if comment else "",
            })

        print("Scraping done.")
        return data

    except Exception as e:
        print("[SCRAPER ERROR] Something went wrong while scraping:")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
