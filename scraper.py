import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

def scrape_amazon(search_query):
    search_query = search_query.replace(" ", "+")  # Format for Amazon URL
    Product_Name = []
    Price = []

    for page_num in range(1, 3):  # Scrape first 2 pages
        url = f"https://www.amazon.in/s?k={search_query}&page={page_num}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()  # Raises an error for non-200 responses
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching page {page_num}: {e}")
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        box = soup.find_all("div", class_="s-main-slot s-result-list s-search-results sg-row")

        for item in box:
            names = item.find_all("h2", class_="a-size-medium a-spacing-none a-color-base a-text-normal")
            prices = item.find_all("span", class_="a-price-whole")

            for i, name in enumerate(names):
                Product_Name.append(name.text.strip())
                Price.append(prices[i].text.strip() if i < len(prices) else "Not Available")

    df = pd.DataFrame({"Product Name": Product_Name, "Prices": Price})

    os.makedirs("static/data", exist_ok=True)  # Ensure the directory exists
    df.to_csv("static/data/amazon_products.csv", index=False, encoding="utf-8")

    return df.to_dict(orient="records")
