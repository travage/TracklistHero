from bs4 import BeautifulSoup
import requests

# Adjust headers to avoid bot detection
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
# Test 1001Tracklist webpage
html_text = requests.get('https://www.1001tracklists.com/tracklist/24gjzlgk/dom-dolla-sahara-coachella-festival-weekend-2-united-states-2024-04-20.html', headers=headers).text
soup = BeautifulSoup(html_text, 'lxml')
print(soup.prettify())


