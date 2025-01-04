#  . .venv/bin/activate
from flask import Flask, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Adjust headers to avoid bot detection
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

# Function should eventually return JSON doc with search results
@app.post('/search')    # http://127.0.0.1:5000/search
def search():
    # Extracts search terms from form data
    request_data = request.form.get('search_terms')
    # Main 1001Tracklist URL for conducting searches
    url = 'https://www.1001tracklists.com/search/result.php'
    payload = {
        'main_search': request_data,
        'search_selection': '9'
    }
    html_response = requests.post(url, data=payload, headers=headers).text
    soup = BeautifulSoup(html_response, 'lxml')

    search_results = {}
    result_num = 1
    # Grab all rows of the results page
    search_row = soup.find_all('div', class_='bItm action oItm')
    for row in search_row:
        title = row.select_one('.bTitle').text.strip()
        search_results[result_num] = title
        result_num += 1

    return search_results

