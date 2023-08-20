const cardAPI = "https://api.pokemontcg.io/v2/cards";
const pageQuery = "?page=";

let firstRun = true;
let totalAmountOfCards = 0;
let cardsPerPage = 250;
let pagesTotal = 0;
let cards = [];

// convert card data json array to Card classes
function convertToCardClasses(data) {
    let _cards = [];
    data.forEach(card => {
        _cards.push(new Card(card));
    });
    return _cards;
}

// fetch cards from API
async function fetchCards(page) {
    const response = await fetch(cardAPI + pageQuery + page);
    const data = await response.json();
    if(firstRun) {
        totalAmountOfCards = data.totalCount;
        pagesTotal = Math.ceil(totalAmountOfCards / cardsPerPage);
        firstRun = false;
    }
    return data.data;
}

// fetch all cards
async function fetchAllCards() {
    let page = 1;
    let _cards = [];

    while(page <= pagesTotal || firstRun) {
        _cards = await fetchCards(page);
        cards = cards.concat(_cards);
        console.log("Page " + page + " fetched. Remaining pages: " + (pagesTotal - page));
        page++;
    }
}

class Card {
    Id;
    Name;
    Images;
    Set;
    PrintingTypes;
    CardMarket;
    Type;
    SubType;
    Rarity


    constructor(card) {
        this.Id = card.id;
        this.Name = card.name;
        this.Type = card.supertype;
        this.SubType = card.subtypes;
        this.Rarity = card.rarity;
        this.PrintingTypes = (card.tcgplayer !== undefined && card.tcgplayer.prices !== undefined) ? Object.keys(card?.tcgplayer?.prices) : null;
        this.CardMarket = (card.cardmarket !== undefined && card.cardmarket.url !== undefined) ? card.cardmarket.url : null;


        this.Images = new CardImages();
        this.Images.small = card.images.small;
        this.Images.large = card.images.large;

        this.Set = new Set();
        this.Set.Id = card.set.id;
        this.Set.Name = card.set.name;
        this.Set.Series = card.set.series;
        this.Set.Number = card.number;
        this.Set.PrintedTotal = card.set.printedTotal;
        this.Set.TotalCards = card.set.total;
        this.Set.Symbol = card.set.images.symbol;
    }
}

class CardImages {
    small;
    large;
}

class Set {
    Id;
    Name;
    Series;
    Symbol;
    Number;
    PrintedTotal;
    TotalCards;
}

// fetch all cards
console.log("Start fetching cards...")
fetchAllCards().then(() => {
    cards = convertToCardClasses(cards);

    // export cards to json file
    fs = require('fs');
    fs.writeFile("api_dataset.json", JSON.stringify(cards), (err) => {
        if(err) {
            console.log(err);
        }
    });
    console.log("Finished fetching cards.");
});