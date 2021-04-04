import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup as bf
import json


def getAllTopics():
    tree = ET.parse('db.xml')
    root = tree.getroot()

    topiclist = []
    for topic in root.findall('topic'):
        topiclist.append(topic.get('name'))
    return topiclist


def getTopic(topic):
    tree = ET.parse('db.xml')
    root = tree.getroot()

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

    tree = ET.parse('db.xml')
    root = tree.getroot()

    for topic in root.findall('topic'):
        # if topic exists, add new note and exit
        if topic.get('name') == note[0]:
            new_note = ET.SubElement(topic, 'note', name=note[1])
            note_txt = ET.SubElement(new_note, '\n\ttext\n\t')
            note_time = ET.SubElement(new_note, '\n\ttimestamp\n\t')
            note_txt.text = note[2]
            note_time.text = note[3]

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

    note_txt.text = note[2]
    note_time.text = note[3]

    try:
        tree.write('db.xml')
        return 1

    except Exception as e:
        print(
            f'Oops, something happened when trying to save changes ({e})')
        return -2


def wikiSearch(page):

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
    DATA = R.json()

    return tuple((DATA[1], DATA[3]))


print(wikiSearch("Jari Kurri"))

print(getTopic('Animal Things'))
