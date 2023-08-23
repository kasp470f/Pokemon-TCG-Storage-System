import json
import math
import requests

from models.card import CardClass

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