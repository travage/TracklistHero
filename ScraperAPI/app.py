#  . .venv/bin/activate
from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Adjust headers to avoid bot detection
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

searchTerms = 'john summit'

@app.route('/search')    # http://127.0.0.1:5000/search
def search():

    url = 'https://www.1001tracklists.com/search/result.php'
    payload = {
        'main_search': searchTerms,
        'search_selection': '9'
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.text
