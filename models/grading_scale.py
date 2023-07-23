# using CGC grading scale
gradingScaleDictionary = {
    10: "Gem Mint",
    9.9: "Mint",
    9.8: "Near Mint/Mint",
    9.6: "Near Mint +",
    9.4: "Near Mint",
    9.2: "Near Mint -",
    9.0: "Very Fine/Near Mint",
    8.5: "Very Fine +",
    8.0: "Very Fine",
    7.5: "Very Fine -",
    7.0: "Fine/Very Fine",
    6.5: "Fine +",
    6.0: "Fine",
    5.5: "Fine -",
    5.0: "Very Good/Fine",
    4.5: "Very Good +",
    4.0: "Very Good",
    3.5: "Very Good -",
    3.0: "Good/Very Good",
    2.5: "Good +",
    2.0: "Good",
    1.8: "Good -",
    1.5: "Fair/Good",
    1.0: "Fair",
    0.5: "Poor",
    0.3: "Poor -",
    0.0: "Insufficient Data"
}

def getGradingScaleName(score: float):
    for key in reversed(sorted(gradingScaleDictionary)):
        if key <= score:
            return gradingScaleDictionary[key]
        