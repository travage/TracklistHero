from flask import Flask
from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET

# Adjust headers to avoid bot detection
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}

app = Flask(__name__)

@app.route('/search')
def search():
    url = 'https://www.1001tracklists.com/search/result.php'
    search_terms = {'main_search': 'john summit', 'search_selection': '9', 'orderby': 'added'}
    response = requests.post(url, json=search_terms, headers=headers)

    #TODO: Current response says the search did not work, POST request needs to be adjusted
    return response.text