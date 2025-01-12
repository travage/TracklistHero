#  . .venv/bin/activate
from flask import Flask, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Adjust headers to avoid bot detection
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

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
    # Fill the dict with all the results
    for row in search_row:
        title = row.select_one('.bTitle').text.strip()
        link = row.find('a').get('href')
        search_results[result_num] = [title, link]
        result_num += 1

    # Flask will send dicts as JSON docs
    return search_results

@app.post('/tracklist')    # http://127.0.0.1:5000/tracklist
def get_tracklist():
    tracklist_url = request.form.get('url')
    tracklist_html = requests.get(tracklist_url, headers=headers).text
    soup = BeautifulSoup(tracklist_html, 'lxml')

    # Test
    # return tracklist_html

    # Grab each row of the tracklist
    tracklist_row = soup.find_all('div', class_='tlpTog')

