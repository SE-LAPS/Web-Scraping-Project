import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.thewhiskyexchange.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

def scrape_product_links():
    url = f"{baseurl}/c/35/japanese-whisky"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_list = soup.find_all("li", {"class": "product-grid__item"})
    product_links = [baseurl + item.find("a")["href"] for item in product_list]
    return product_links

def scrape_product_details(product_url):
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_name = soup.find("h1", {"class": "product-main__name"}).text.strip()
    product_price = soup.find("p", {"class": "product-action__price"}).text.strip()
    product_rating = soup.find("span", {"class": "review-overview__rating"}).text.strip()
    return {"Name": product_name, "Price": product_price, "Rating": product_rating}

def main():
    product_links = scrape_product_links()
    product_data = []
    for link in product_links:
        product_data.append(scrape_product_details(link))

    df = pd.DataFrame(product_data)
    df.to_csv("whisky_products.csv", index=False)
    print("Data Saved To whisky_products.csv")

if __name__ == "__main__":
    main()
