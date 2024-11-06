import requests
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url = 'https://finance.yahoo.com/news/djt-stock-surges-following-elon-musk-cameo-at-trump-rally-161321275.html'  # Replace this with the actual URL

# Fetch the content from the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the <time> tag and print its text
time_tag = soup.find('time')
if time_tag:
    print("Text in time tag:", time_tag.text)
else:
    print("No <time> tag found")

p_tags= soup.find_all('p')

for i in p_tags:
    print(i.text)
    print("\n")
