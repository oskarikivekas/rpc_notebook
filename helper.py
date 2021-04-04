import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup as bf
import json


def getAllTopics():
    try:

        tree = ET.parse('db.xml')
        root = tree.getroot()

        topiclist = []
        for topic in root.findall('topic'):
            topiclist.append(topic.get('name'))

    except Exception:
        print("Error when trying to read database contents")

    return topiclist

# searches for topic and if it finds one, returns all notes under it.


def getTopic(topic):
    try:
        tree = ET.parse('db.xml')
        root = tree.getroot()

    except Exception:
        print("Error when trying to read xml contents")

    notelist = []
    t = root.find("./topic[@name='%s']" % topic)
    if t == None:
        return "No match"
    for note in t:
        name = note.get('name')
        txt = note.find('text').text
        time = note.find('timestamp').text
        notelist.append(tuple((name, txt, time)))
    return notelist


def addNewNote(note):

    try:
        tree = ET.parse('db.xml')
        root = tree.getroot()

    except Exception:
        print("Error when trying to read xml contents")

    for topic in root.findall('topic'):
        # if topic exists, add new note and exit

        if topic.get('name') == note[0]:
            new_note = ET.SubElement(topic, 'note', name=note[1])
            note_txt = ET.SubElement(new_note, 'text')
            note_time = ET.SubElement(new_note, 'timestamp')
            note_txt.text = "\n\t"+note[2]+"\n\t"
            note_time.text = "\n\t"+note[3]+"\n\t"

            try:
                tree.write('db.xml')
                return 0
            except Exception as e:
                print(
                    f'Oops, something happened when trying to save changes ({e})')
                return -1

    # "else" create topic and add new note

    new_topic = ET.SubElement(root, 'topic', name=note[0])
    new_note = ET.SubElement(new_topic, 'note', name=note[1])

    note_txt = ET.SubElement(new_note, 'text')
    note_time = ET.SubElement(new_note, 'timestamp')

    note_txt.text = ("\n\t"+note[2]+"\n\t")
    note_time.text = ("\n\t"+note[3]+"\n\t")

    try:
        tree.write('db.xml')
        return 1

    except Exception as e:
        print(
            f'Oops, something happened when trying to save changes ({e})')
        return -2


def wikiSearch(page):
    try:

        S = requests.Session()

        URL = "https://en.wikipedia.org/w/api.php"

        PARAMS = {
            "action": "opensearch",
            "namespace": "0",
            "search": page,
            "limit": "1",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS)

    except Exception:
        print("")
    DATA = R.json()
    # return topic and link, results limited to one for convenience :P
    return tuple((DATA[1], DATA[3]))
