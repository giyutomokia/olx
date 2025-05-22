import requests
from bs4 import BeautifulSoup
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

url = "https://www.olx.in/items/q-car-cover"

print("Sending request to OLX search page...")
response = requests.get(url, headers=headers)
print(f"Status Code: {response.status_code}")

if response.status_code != 200:
    print("Failed to load the page.")
    exit()

soup = BeautifulSoup(response.content, 'lxml')
items = soup.find_all("li", class_="css-19ucd76")  # Each listing

results = []
for item in items:
    title_tag = item.find("span", class_="css-1bjwylw")
    price_tag = item.find("span", class_="css-1eoo2p1")
    location_tag = item.find("span", class_="css-17gebsw")
    link_tag = item.find("a", href=True)

    if title_tag and price_tag and location_tag and link_tag:
        title = title_tag.text.strip()
        price = price_tag.text.strip()
        location = location_tag.text.strip()
        url = "https://www.olx.in" + link_tag['href']

        results.append({
            "title": title,
            "price": price,
            "location": location,
            "url": url
        })

# Save to CSV
csv_file = "olx_car_covers.csv"
keys = ["title", "price", "location", "url"]
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(results)

print(f"Scraped {len(results)} car cover listings.")
print(f"Saved to '{csv_file}'")
