import pandas as pd
import requests
from bs4 import BeautifulSoup

Product_Name = []
Price = []

for page_num in range(1, 3):  # Limiting to 2 pages for demo (change to 10)
    url = f"https://www.amazon.in/s?k=iphone+16&page={page_num}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
    else:
        print(f"Failed to retrieve page {page_num}. Status code: {r.status_code}")
        continue

    box = soup.find_all("div", class_="s-main-slot s-result-list s-search-results sg-row")

    for item in box:
        names = item.find_all("h2", class_="a-size-medium a-spacing-none a-color-base a-text-normal")
        prices = item.find_all("span", class_="a-price-whole")

        for i, name in enumerate(names):
            Product_Name.append(name.text.strip())
            Price.append(prices[i].text.strip() if i < len(prices) else "Not Available")

df = pd.DataFrame({"Product Name": Product_Name, "Prices": Price})
df.to_csv("amazon_products.csv", index=False, encoding="utf-8")
print("Scraping complete. Data saved to amazon_products.csv.")
