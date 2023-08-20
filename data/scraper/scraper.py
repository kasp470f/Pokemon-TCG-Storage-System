import json
import math
import requests


class CardImagesClass:
    small: str
    large: str

class SetClass:
    Id: int
    Name: str
    Series: str
    Symbol: str
    Number: int
    PrintedTotal: int
    TotalCards: int

class CardClass:
    Id: int
    Name: str
    Images: CardImagesClass
    Set: SetClass
    PrintingTypes: list | None
    CardMarket: str
    Type: str
    SubType: str
    Rarity: str

    def __init__(self, card: any):
        self.Id = card["id"];
        self.Name = card["name"];
        self.Type = card["supertype"];
        self.SubType = card["subtypes"];
        self.Rarity = card["rarity"] if "rarity" in card else None;
        self.PrintingTypes = self.getPrintingTypes(card);
        self.CardMarket = self.getCardMarketLink(card);

        self.Images = CardImagesClass();
        self.Images.small = card["images"]["small"];
        self.Images.large = card["images"]["large"];

        self.Set = SetClass();
        self.Set.Id = card["set"]["id"];
        self.Set.Name = card["set"]["name"];
        self.Set.Series = card["set"]["series"];
        self.Set.Symbol = card["set"]["images"]["symbol"];
        self.Set.Number = card["number"];
        self.Set.PrintedTotal = card["set"]["printedTotal"];
        self.Set.TotalCards = card["set"]["total"];

    def getPrintingTypes(self, card: any):
        if "tcgplayer" in card:
            if card["tcgplayer"] != None:
                if "prices" in card["tcgplayer"]:
                    if card["tcgplayer"]["prices"] != None:
                        return list(card["tcgplayer"]["prices"].keys());
        return None;

    def getCardMarketLink(self, card: any):
        if "cardmarket" in card:
            if card["cardmarket"] != None:
                if "url" in card["cardmarket"]:
                    if card["cardmarket"]["url"] != None:
                        return card["cardmarket"]["url"];
        return None;

cardAPI = "https://api.pokemontcg.io/v2/cards";
pageQuery = "?page=";

firstRun = True;
totalAmountOfCards = 0;
cardsPerPage = 250;
pagesTotal = 0;
cards = [];

# convert card data json array to Card classes
def convertToCardClasses(data: []):
    _cards = [];
    # foreach card in data array
    for card in data:
        # create new card class
        _cards.append(CardClass(card));

    return _cards;

# fetch cards from API
def fetchCards(page):
    global firstRun;
    response = requests.get(cardAPI + pageQuery + str(page));
    data = response.json();

    if firstRun == True:
        global totalAmountOfCards;
        totalAmountOfCards = data["totalCount"];
        global pagesTotal;
        pagesTotal = math.ceil(totalAmountOfCards / cardsPerPage);
        firstRun = False;

    return data["data"];

# fetch all cards
def fetchAllCards():
    global pagesTotal, firstRun, cards;
    page = 1;
    _cards = [];

    while page <= pagesTotal or firstRun:
        _cards = fetchCards(page);
        cards += _cards;
        print("Fetched page " + str(page) + " of " + str(pagesTotal) + " pages.");
        page += 1;



print("Fetching cards...");
fetchAllCards()
cards = convertToCardClasses(cards)

# export cards to json file
card_dicts = []
for card in cards:
    card_dict = card.__dict__
    card_dict['Images'] = card.Images.__dict__
    card_dict['Set'] = card.Set.__dict__
    card_dicts.append(card_dict)

with open("api_dataset.json", "w") as f:
    json.dump(card_dicts, f)

print("Finished fetching cards.")