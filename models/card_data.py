import datetime
from models.grading_models import RawGrading

class CardDto:
    Id: int = None
    CardImage: str = None
    CardId: str = None
    Name: str = None
    CardType: str = None
    CardSubType: str = None
    CardSetId: str = None
    Rarity: str = None
    SetSymbol: str = None
    SetName: str = None
    PrintingType: str = None
    Condition = None
    ConditionNotes: str = None
    Grading: RawGrading = None
    Location: str = None
    DateObtained: datetime = None
    ObtainedHow: str = None
    CardMarket: str = None
    Comment: str = None

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

    def toSheetRow(self):
        list = [self.toImage(self.CardImage), self.CardId, self.Name, self.toType(), self.CardSetId, self.Rarity, self.toImage(self.SetSymbol), self.SetName, self.PrintingType, self.toCondition(), self.Location, self.toStringDate(), self.toCardMarket(), self.Comment]
        for i in range(len(list)):
            if list[i] is None:
                list[i] = ""

        return [str(x) for x in list]