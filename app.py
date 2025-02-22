#  . .venv/bin/activate
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import os

def create_app():
    app = Flask(__name__)

# Adjust headers to avoid bot detection
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

    @app.post('/search')    # http://127.0.0.1:5000/search used in developemtn
    def search():
        try:
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

            return jsonify(search_results)

        except Exception as e:
            return jsonify({'error': str(e)})

    @app.post('/tracklist')    # http://127.0.0.1:5000/tracklist used in development
    def get_tracklist():
        try:
            tracklist_url = request.form.get('url')
            tracklist_html = requests.get(tracklist_url, headers=headers).text
            soup = BeautifulSoup(tracklist_html, 'lxml')

            # Grab each row of the tracklist
            tracklist_row = soup.find_all('div', class_='tlpTog')
            # Keeps track of the row number
            counter = 1
            tracklist = {}
            for row in tracklist_row:
                # Some rows will not have HTML elements with the specified HTML classes,
                # in which case bs4 sets the variable to None.
                # Since the text is being extracted from the HTML element, an exception
                # will occur if the variable is None.
                try:
                    track_position = row.select_one('.fontXL').text.strip()
                except:
                    track_position = '-'  # No track_position means the track is part of the mashup above it

                try:
                    timestamp = row.select_one('.cue.noWrap.action.mt5').text.strip()  # Sometimes the tag is there but has no text, so timestamp = ''
                except:
                    timestamp = 'NA'

                try:
                    track = row.select_one('.trackValue').text.strip()
                except:
                    track = 'NA'

                # Captures version (edit) of the song (e.g. acapella, intro edit, etc.)
                try:
                    edit_data = row.select_one('.trackEditData').text.strip()
                except:
                    edit_data = 'NA'

                tracklist[counter] = [track_position, timestamp, track, edit_data]
                counter += 1

            return jsonify(tracklist)

        except Exception as e:
            return jsonify({'error': str(e)})

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)