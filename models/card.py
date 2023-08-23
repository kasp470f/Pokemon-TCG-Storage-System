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