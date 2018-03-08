import requests
import json

from .. import config

class AnkiConnectorUtils:

    def __init__(self, url):
        self.url = url

    def makeRequest(self, action:str, parmeters:dict={} ):

        payload = self._buildPayload(action, parmeters)
        print("Parameters send to Anki", payload)
        #TODO log payloads
        try:
            res = requests.post(self.url, payload)
        except Exception as e:
            print(e.message)
            print("An error has occoured make the request.")

        if res.status_code == 200:
            data = json.loads(res.text)
            return data["result"]
        else:
            error = res.status_code
            return error

    def getDeckNames(self):
        decks = self.makeRequest("deckNames")
        return decks

    def createDeck(self, deckName):
        decks = self.makeRequest("createDeck", {"deck": deckName})
        return decks

    def uploadNotes(self, notes):
        result = self.makeRequest("addNotes", notes)
        return result

    def testConnection(self):
        try:
            req = requests.post(self.url, data={})
            #TODO log status code
            return req.status_code == 200
        except requests.exceptions.RequestException:
            #TODO log excpetion
            return False


    def _buildPayload(self, action, params={}, version=5):
        payload = {}
        payload["action"] = action
        payload["params"] = params
        payload["version"] = version
        print(payload)
        return json.dumps(payload)


if __name__ == "__main__":
    a = AnkiConnectorUtils("http://127.0.0.1:8765/")
    param =  {"note": {"deckName": "Default", "modelName": "Basic", "fields": { "Front": "front content 4", "Back": "back content"}}}

    result = a.makeRequest("addNote", param)
    print("Results \n\n")
    print(result)
