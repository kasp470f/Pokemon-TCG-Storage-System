import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime


class CardData:
    CardImage = None
    CardId = None
    Name = None
    CardType = None
    CardSubType = None
    CardSetId = None
    Rarity = None
    SetSymbol = None
    SetName = None
    PrintingType = None
    Condition = None
    ConditionNotes = None
    Location = None
    DateObtained = None
    ObtainedHow = None
    CardMarket = None
    Comment = None

    def __init__(self, card):
        self.CardImage = card['Images']['large']
        self.CardId = card['Id']
        self.Name = card['Name']
        self.SetName = card['Set']['Name']
        self.Rarity = card['Rarity']
        self.CardMarket = card['CardMarket']
        self.CardType = card['Type']
        self.CardSubType = card['SubType']
        self.SetSymbol = card['Set']['Symbol']

        if str(card['Set']['Number']).isnumeric():
            self.CardSetId = f"{str(card['Set']['Number'])} / {str(card['Set']['PrintedTotal'])} ({str(card['Set']['TotalCards'])})"
        else:
            # get the characters in the string before the first number and put them in a new string 
            cardSubset = ''.join([i for i in card['Set']['Number'] if not i.isdigit()])
            self.CardSetId = f"{str(card['Set']['Number'])} / {cardSubset}{str(card['Set']['TotalCards'])}"

    def __str__(self):
        return f"CardId: {self.CardId}\nName: {self.Name}\nCardType: {self.CardType}\nCardSetNumbers: {self.CardSetNumbers}\nSetName: {self.SetName}\nPrintingType: {self.PrintingType}\nCondition: {self.Condition}\nConditionNotes: {self.ConditionNotes}\nLocation: {self.Location}\nDateObtained: {self.DateObtained}\nCardMarket: {self.CardMarket}\nComment: {self.Comment}"
    
    def toCondition(self):
        if self.Condition == 1:
            return "Mint"
        elif self.Condition == 2:
            return "Near Mint"
        elif self.Condition == 3:
            return "Light Played"
        elif self.Condition == 4:
            return "Played"
        elif self.Condition == 5:
            return "Damaged"
        else:
            return None
        
    def toImage(self, image):
        return f'=IMAGE("{image}")'
    
    def toCardMarket(self):
        if self.CardMarket is None:
            return None
        else:
            return f'=HYPERLINK("{self.CardMarket}", "{self.Name} - CardMarket")'
        
    def toStringDate(self):
        if type(self.DateObtained) is datetime.date:
            return self.DateObtained.strftime("%d %B, %Y")
        else:
            return "Unknown" 
    
    def toType(self):
        if self.CardType == "Pok\u00c3\u00a9mon":
            return "Pokémon"
        
        return f"{self.CardType} ({self.CardSubType[0]})";

    def toSheetRow(self, addedAs):
        list = [self.toImage(self.CardImage), self.CardId, self.Name, self.toType(), self.CardSetId, self.Rarity, self.toImage(self.SetSymbol), self.SetName, self.PrintingType, self.toCondition(), self.Location, self.toStringDate(), self.toCardMarket(), self.Comment, addedAs]
        for i in range(len(list)):
            if list[i] is None:
                list[i] = ""

        return [str(x) for x in list]

class GoogleSheets:

    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("sheets_crendentials.json", scope)
        client = gspread.authorize(credentials)
        self.sheet = client.open("Pokémon Storage Database").get_worksheet_by_id(0)

    def addCardExtended(self, card):
        insertRow = card.toSheetRow("Extended")
        self.sheet.insert_row(insertRow, 2, value_input_option='USER_ENTERED')
        rowNumber = self.sheet.find(card.CardId).row
        self.sheet.insert_note(f'J{rowNumber}', card.ConditionNotes)
        self.sheet.insert_note(f'O{rowNumber}', "Condition is almost always accurate for extended cards. A indepth look at the card has been done and the condition is checked with a microscope.")

    def addCardBulk(self, card):
        insertRow = card.toSheetRow("Bulk")
        self.sheet.insert_row(insertRow, 2, value_input_option='USER_ENTERED')
        rowNumber = self.sheet.find(card.CardId).row
        self.sheet.insert_note(f'J{rowNumber}', card.ConditionNotes)
        self.sheet.insert_note(f'O{rowNumber}', "Condition is not always accurate for bulk cards, so if you want I can take a look at the card and update the condition if needed.")