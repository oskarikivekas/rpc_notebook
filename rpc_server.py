# https://docs.python.org/3/library/xmlrpc.server.html#module-xmlrpc.server
# https://docs.python.org/3/library/socketserver.html#socketserver.ThreadingMixIn
# https://docs.python.org/3/library/xml.etree.elementtree.html

# NOTE: These xml modules are not safe, do not run this server if possibility of prosessing untrusted data is present!

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn
import time
import helper

# Threadingmixin


class ThreadedServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


# Restriction for path requests
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# When server is called by client, requesthandler creates a connenction which then is passed to ThreadedServer class.
# This class implements threadingmixin which creates a thread for each client.


# Clientfunctions class handles the client rpc commands and then passes parameters to helper containing the functionality

# Server runs at localhost:8000 and is asynchronous
with ThreadedServer(('127.0.0.1', 8000), requestHandler=RequestHandler) as server:

    # add default functions
    server.register_introspection_functions()

    # contains functions available for clients
    class Clientfunctions:

        def serverOnline(self):
            return "Server is running.."

        def newNote(self, note):
            returnvalue = helper.addNewNote(note)
            if returnvalue == 0:
                return ("Your note was added succesfully!")
            elif returnvalue == -2:
                return("Your note could not be saved! Try again.")
            else:
                return ("New topic was created and your note added!")

        def readNote(self, topic):
            data = helper.getTopic(topic)
            return data

        def getTopics(self):
            return (helper.getAllTopics())

        def wikiSearch(self, page):
            wikidata = helper.wikiSearch(page)
            return wikidata

        def addLink(self, topic, link):
            helper.addLink(topic, link)
            return "Success"

    # register functions to be called by rpc client
    server.register_instance(Clientfunctions())

    class TestFunctions:

        def test(self, value):
            return (f'Test succesful, value: {value}')

        def testsleep(self, length):
            time.sleep(length)
            return ("READY")

    """Remove # to enable testfunctions"""
    # server.register_instance(TestFunctions())

    server.serve_forever()
