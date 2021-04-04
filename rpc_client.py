import xmlrpc.client
from datetime import datetime


s = xmlrpc.client.ServerProxy('http://127.0.0.1:8000')

# Nothing fancy here, just menu prints and then function calls. Some input validation aswell.

try:

    def newNote():

        topic = input("Give a topic for the note: ")
        if len(topic) < 2:
            print("Topic has to have atleast 2 characters!")
            return 1

        print(f" > {topic} <\n")

        header = input('Give a name for the note: ')
        if len(header) < 2:
            print("Name has to have atleast 2 characters!")
            return 1

        text = input("Note: ")
        if len(text) < 3:
            print("Text has to have atleast 3 characters!")
            return 1

        timestamp = datetime.today().strftime("%m/%d/%y - %H:%M:%S")
        note = [topic, header, text, timestamp]
        print(s.newNote(note))

    def noteReader():
        while (True):
            print("------------------------------------------")
            print("\n   >NOTES<")
            print("1.) Search notes\n",
                  "2.) Show all topics\n",
                  "0.) Return to menu\n")
            c = int(input("choose: "))

            if c == 1:
                topic = input("Give a topic: ")
                notes = s.readNote(topic)
                print("\n------------------------------------------")

                if (notes == "No match"):
                    print("No match, try another one!")
                    continue
                else:
                    for i in range(len(notes)):
                        print(
                            f"Note: {notes[i][0]}\n{notes[i][1]}{notes[i][2]}\n")

            elif c == 2:
                topics = s.getTopics()
                print("Notebook topics:")
                for i in topics:
                    print(f"\n{i}")

            elif c == 0:
                main()
            else:
                print("Oops, wrong option... Try again!")

    def wikiSearch():
        page = input("Give the topic you want to search: ")
        results = s.wikiSearch(page)

        print("Search results:\n")
        for i in range(len(results[0])):
            print(f"{results[0][i]}")
        print("Do you want to add this page link to notebook?")

        yes_no = input("Y/N:")
        if yes_no == ("Y" or "y"):
            appendLink(results)

    def appendLink(results):
        topics = s.getTopics()
        print("Notebook topics:")
        for i in topics:
            print(f"\n{i}")

        i_topic = input("Type in the topic you want link to be added: ")

        timestamp = datetime.today().strftime("%m/%d/%y - %H:%M:%S")
        note = [i_topic, results[0][0],
                f"Wikipedia link: {results[1][0]}", timestamp]
        print(s.newNote(note))

    def main():
        while(True):
            print("-------------------------------")
            print("\n    >NOTEBOOK<\n")
            print(" 1.) Add a new note\n",
                  "2.) Read notes\n",
                  "3.) Search for wikipedia article\n",
                  "0.) Quit\n")

            c = input("What do u want to do: ")
            if c.isdigit():
                if c == '1':
                    newNote()

                elif c == '2':
                    noteReader()

                elif c == '3':
                    wikiSearch()

                elif c == '0':
                    print("Closing..")
                    exit(1)
                else:
                    print("\nIncorrect input, try again!\n")
            else:
                print("Give a correct number!")

    s.serverOnline()
    main()

except Exception:
    print("\nServer is currently unavailable, try again later!\n")
    exit(2)
