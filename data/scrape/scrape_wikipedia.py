import requests
import json
from bs4 import BeautifulSoup

# Wikipedia URL (Replace this with your desired Wikipedia page)
url = "https://en.wikipedia.org/wiki/Buffett_indicator"  # Change to your Wikipedia page

# Set headers to avoid bot detection
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Fetch the webpage
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Dictionary to store extracted data
wiki_data = {}

# Find the main content div
content_div = soup.find("div", {"id": "mw-content-text"})

if content_div:
    current_section = "Introduction"  # Start with introduction if no <h2> before paragraphs
    wiki_data[current_section] = []

    # Loop through all elements in the main content div
    for element in content_div.find_all(["h2", "h3", "p", "ul", "ol", "table"]):
        if element.name in ["h2", "h3"]:
            # Get section title and remove [edit] button text
            current_section = element.text.replace("[edit]", "").strip()
            wiki_data[current_section] = []
        elif element.name == "p":
            # Append paragraph text to the current section
            text = element.text.strip()
            if text:
                wiki_data[current_section].append(text)
        elif element.name in ["ul", "ol"]:
            # Convert lists to bullet points
            list_items = [li.text.strip() for li in element.find_all("li")]
            if list_items:
                wiki_data[current_section].extend(list_items)
        elif element.name == "table":
            # Indicate a table is present in this section
            wiki_data[current_section].append("[Table found]")

# Remove empty sections
wiki_data = {k: v for k, v in wiki_data.items() if v}

# Save the extracted content into a JSON file
with open("../books/the_buffet_indicator.json", "w", encoding="utf-8") as file:
    json.dump(wiki_data, file, indent=4, ensure_ascii=False)

print("Wikipedia data saved to the_buffet_indicator.json")
