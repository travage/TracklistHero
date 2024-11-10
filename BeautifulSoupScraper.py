from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET

# Adjust headers to avoid bot detection
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
# Test 1001Tracklist webpages
html_text = requests.get('https://www.1001tracklists.com/tracklist/24gjzlgk/dom-dolla-sahara-coachella-festival-weekend-2-united-states-2024-04-20.html', headers=headers).text
# html_text = requests.get('https://www.1001tracklists.com/tracklist/13wh8wm1/rl-grime-knock2-silo-dallas-united-states-2024-10-25.html', headers=headers).text
# html_text = requests.get('https://www.1001tracklists.com/tracklist/rq05l8k/chasewest-avant-gardner-new-york-united-states-2023-02-04.html', headers=headers).text
soup = BeautifulSoup(html_text, 'lxml')

# Create XML tree root
root = ET.Element('songs')

# Keeps track of the row number
counter = 1
def add_songs(row_num, position, time, name, edit):
    song = ET.SubElement(root, 'song', row=str(row_num))
    position_elem = ET.SubElement(song, 'position')
    position_elem.text = position
    time_elem = ET.SubElement(song, 'timestamp')
    time_elem.text = time
    name_elem = ET.SubElement(song, 'name')
    name_elem.text = name
    edit_elem = ET.SubElement(song, 'version')
    edit_elem.text = edit

# Grab each row of the tracklist
tracklist_row = soup.find_all('div', class_='tlpTog')
# Extract the track position, the timestamp, the track
# (includes artist and song) from each row, and edit data from each row
for row in tracklist_row:
    # Some rows will not have HTML elements with the specified classes,
    # in which case bs4 sets the variable to None.
    # Since the text is being extracted from the HTML element, an exception
    # will occur if the variable is None.
    try:
        track_position = row.select_one('.fontXL').text.strip()
    except:
        track_position = '-'    # No track_position means the track is part of the mashup above it

    try:
        timestamp = row.select_one('.cue.noWrap.action.mt5').text.strip()   # Sometimes the tag is there but has no text, so timestamp = ''
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

    add_songs(counter, track_position, timestamp, track, edit_data)
    counter += 1

tree = ET.ElementTree(root)
# tree.write('')
