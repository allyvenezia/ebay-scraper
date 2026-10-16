import json
import argparse
from bs4 import BeautifulSoup
import requests

parser = argparse.ArgumentParser(description="Download eBay listings as JSON")
parser.add_argument("--search", required=True) 
parser.add_argument("--pages-dir")
args = parser.parse_args()

print("searching for:", args.search)

listings = []


for page_num in range(1, 11):
    if args.pages_dir:
        path = args.pages_dir + "/page-" + str(page_num) + ".html"
        with open(path, encoding="utf-8") as f:
            html = f.read()
    else: 
        response = requests.get("https://www.ebay.com/sch/i.html", 
                        params={"_nkw": args.search, "_pgn": page_num},
                        headers = {"User-Agent": "Mozilla/5.0"},
                        timeout = 10)
        html = response.text



    soup = BeautifulSoup(html, "html.parser")
    for item in soup.select(".s-item"):
        name = item.select_one(".s-item__title")
        if name:
            name = name.get_text()
        else:
            name = None

        price = item.select_one(".s-item__price")
        if price:
            price = price.get_text(strip=True).split(" to ")[0]
            price = price.replace("$", "").replace(",", "")
            dollars, cents = price.split(".")
            price = int(dollars) * 100 + int(cents)
        else:
            price = None

        status = item.select_one(".SECONDARY_INFO")
        if status:
            status = status.get_text()
        else:
            status = None

        shipping = item.select_one(".s-item__shipping")
        if shipping is None:
            shipping = None
        elif shipping and "free" in shipping.get_text().lower():
            shipping = 0
        else:
            shipping = shipping.get_text().lower().replace("shipping", "").replace("from", "")
            shipping = shipping.replace("$", "").replace("+", "").replace(",", "").strip()
            dollars, cents = shipping.split(".")
            shipping = int(dollars) * 100 + int(cents)

        free_returns = item.select_one(".s-item__free-returns")
        if free_returns and "free returns" in free_returns.get_text().lower():
            free_returns = True
        elif free_returns is None:
            free_returns = None
        else:
            free_returns = False

        items_sold = item.select_one(".s-item__hotness")
        if items_sold and "sold" in items_sold.get_text().lower():
            items_sold = int(items_sold.get_text().split()[0].replace(',', ''))
        else:
            items_sold = None

        listings.append({
            "name": name,
            "price": price,
            "status": status,
            "shipping": shipping,
            "free_returns": free_returns,
            "items_sold": items_sold,
        })



print("Total Listings:", len(listings))

with open(args.search + ".json", "w", encoding="utf-8") as f:
    json.dump(listings, f, indent=2)