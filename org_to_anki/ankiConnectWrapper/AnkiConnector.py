from .AnkiConnectorUtils import AnkiConnectorUtils
from ..ankiClasses import AnkiQuestion
from .. import config

class AnkiConnector:

    def __init__(self, url=config.defaultAnkiConnectAddress, defaultDeck=config.defaultDeck):
        self.url = url #TODO remove
        self.defaultDeck = defaultDeck
        self.currentDecks = []
        self.connector = AnkiConnectorUtils(self.url)

    def uploadNewQuestions(self, questions):

        if self.connector.testConnection() != True:
            print("Failed to connect to Anki Connect. Ensure Anki is open and AnkiConnect is installed")
            return False

        self._checkForDefaultDeck()
        self._buildNewDecksAsRequired(questions)
        # Build new questions
        notes = self._buildNotes(questions)

        # TODO Get all question from that deck and use this to verify questions need to be uploaded
        # self._removeAlreadyExistingQuestions()

        # Insert new question through the api
        self.connector.uploadNotes(notes)

    def _buildNewDecksAsRequired(self, newNotes):
        # Check decks exist for notes
        newDeckPaths = []
        for i in newNotes:
            fullDeckPath = self._getFullDeckPath(i.deckName)
            if fullDeckPath not in self.currentDecks and fullDeckPath not in newDeckPaths:
                newDeckPaths.append(fullDeckPath)

        # Create decks
        for deck in newDeckPaths:
            self._createDeck(deck)


    def _getFullDeckPath(self, deckName):
        return self.defaultDeck + "::" + deckName

    def _checkForDefaultDeck(self):
        self.currentDecks = self.connector.getDeckNames()
        if self.defaultDeck not in self.currentDecks:
            self._createDeck(self.defaultDeck)

    def _buildNotes(self, ankiQuestions):

        notes = []
        for i in ankiQuestions:
            notes.append(self._buildNote(i))

        finalNotes = {}
        finalNotes["notes"] = notes
        return finalNotes

    def _buildNote(self, ankiQuestion):

        if isinstance(ankiQuestion, AnkiQuestion.AnkiQuestion):
            # All decks stored under default deck
            if ankiQuestion.deckName == "" or ankiQuestion.deckName == None:
                # TODO log note was built on default deck
                deckName = self.defaultDeck
            else:
                deckName = self._getFullDeckPath(ankiQuestion.deckName)

            # Convert
            note = {"deckName": deckName, "modelName": "Basic"}
            note["tags"] = ankiQuestion.tags

            # Generate fields
            fields = {}
            fields["Front"] = ankiQuestion.question
            fields["Back"] = self._createAnswerString(ankiQuestion.answers)

            note["fields"] = fields

        else:
            # TODO log issue
            raise Exception(
                "Object %s is not an instance of AnkiQuestion and cannot be converted to note" % (ankiQuestion))

        return note

    def _createAnswerString(self, answers, bulletPoints=True):
        result = ""
        if bulletPoints == False:
            for i in answers:
                result += i + "<br>"  # HTML link break
        else:
            # Can only can create single level of indentation. Align bulletpoints.
            result += "<ul style='list-style-position: inside;'>"
            for i in answers:
                result += "<li>" + i + "</li>"
            result += "</ul>"
        return result


if __name__ == "__main__":

    b = AnkiConnectBridge()
    b._getDeckNames()

    # TestQuestion
    # q = AnkiQuestion("Test question", "Basic")
    # q.addAnswer("First answer edited")
    # q.addAnswer("Second answer")
    # a = AnkiQuestion("second test question", "Basic")
    # a.addAnswer("First answer")
    # a.addAnswer("Second answer")
    # b.uploadNewQuestions([q])#, a])