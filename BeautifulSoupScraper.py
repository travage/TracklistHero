from bs4 import BeautifulSoup
import requests
# Regex
import re
import xml.etree.ElementTree as ET

# Adjust headers to avoid bot detection
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
# Test 1001Tracklist webpage
html_text = requests.get('https://www.1001tracklists.com/tracklist/24gjzlgk/dom-dolla-sahara-coachella-festival-weekend-2-united-states-2024-04-20.html', headers=headers).text
soup = BeautifulSoup(html_text, 'lxml')

# # Create XML tree root
# root = ET.Element('songs')

# Grab each row of the tracklist
tracklist_row = soup.find_all('div', attrs={'data-trno': re.compile(r'\d+')})
# Extract the track number, the timestamp, and the track
# (includes artist and song) from each row.
for row in tracklist_row:
    # Some rows will not have HTML elements with the specified classes,
    # in which case bs4 sets the variable to None.
    # Since the text is being extracted from the HTML element, an exception
    # will occur if the variable is None.
    try:
        track_num = row.select_one('.fontXL').text.strip()
    except:
        track_num = 'NA'

    try:
        timestamp = row.select_one('.cue.noWrap.action.mt5').text.strip()
    except:
        timestamp = 'NA'

    try:
        track = row.select_one('.notranslate.blueTxt, .notranslate.redTxt').text.strip()
    except:
        track = 'NA'

    print(f'{track_num}. {track} {timestamp}')