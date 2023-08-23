import datetime
from models.grading_models import RawGrading
from models.location_dto import LocationDto

class CardDto:
    Id: int = None
    CardImage: str = None
    CardId: str = None
    Name: str = None
    Type: str = None
    SubType: str = None
    SetId: str = None
    Rarity: str = None
    SetId: str = None
    PrintingType: str = None
    Condition = None
    ConditionNotes: str = None
    Location: LocationDto = None
    DateObtained: datetime = None
    ObtainedHow: str = None
    CardMarket: str = None
    Comment: str = None

    def __init__(self, card):
        self.CardImage = card['Images']['large']
        self.CardId = card['Id']
        self.Name = card['Name']
        self.Rarity = card['Rarity']
        self.SetId = card['Set']['Id']
        self.CardMarket = card['CardMarket']
        self.Type = card['Type']
        self.SubType = card['SubType'][0]

        if str(card['Set']['Number']).isnumeric():
            self.CardSetId = f"{str(card['Set']['Number'])} / {str(card['Set']['PrintedTotal'])} ({str(card['Set']['TotalCards'])})"
        else:
            # get the characters in the string before the first number and put them in a new string 
            cardSubset = ''.join([i for i in card['Set']['Number'] if not i.isdigit()])
            self.CardSetId = f"{str(card['Set']['Number'])} / {cardSubset}{str(card['Set']['TotalCards'])}"
    
    def getType(self):
        if self.Type == "Pok\u00c3\u00a9mon":
            return "Pokémon"
        
        return self.Type;

    def getSubType(self):
        if self.Type == "Trainer":
            return self.SubType
        
        return None
