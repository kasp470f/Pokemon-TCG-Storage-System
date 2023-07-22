import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheets:

    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("sheets_crendentials.json", scope)
        client = gspread.authorize(credentials)
        self.sheet = client.open("Pokémon Storage Database").get_worksheet_by_id(0)

    def addCardToDatabase(self, card):
        insertRow = card.toSheetRow("Extended")
        self.sheet.insert_row(insertRow, 2, value_input_option='USER_ENTERED')
        rowNumber = self.sheet.find(card.CardId).row
        self.sheet.insert_note(f'J{rowNumber}', card.ConditionNotes)
        self.sheet.insert_note(f'O{rowNumber}', "Condition is almost always accurate for extended cards. A indepth look at the card has been done and the condition is checked with a microscope.")