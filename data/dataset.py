import json
from urllib.request import Request, urlopen;
import cv2 as cv;
import numpy as np

from models.card import CardClass;

hamming_distance_threshold = 80;
matches_length = 5;

read_dataset = open('data/hash_dataset.json', 'r')

# parse the json file
dataset = json.load(read_dataset)

def hashString_to_array(hashstring):
    # split the string into an array of characters
    hasharray = list(hashstring)
    # convert the array of characters into an array of booleans
    hasharray = [True if x == '1' else False for x in hasharray]
    return hasharray

def findMatch(image) -> CardClass | None:
    hash = toHash(image)

    matches = []
    # loop through the dataset
    for card in dataset:
        # find the hamming distance between the hash and the card's hash if it exists
        if 'Hash' in card:
            hamming_distance = np.count_nonzero(np.array(hashString_to_array(card['Hash'])) != np.array(hash))
            # keep only the 5 best matches (lowest hamming distance) in the matches array if a match is found with a hamming distance lower than the threshold and it has a lower hamming distance than the last card in the list then push it to the list in the correct position (sorted by hamming distance) and remove the last card in the list
            if hamming_distance < hamming_distance_threshold and (len(matches) < matches_length or hamming_distance < matches[-1]['HammingDistance']):
                matches.append({ "HammingDistance": hamming_distance, "Card": card})
                matches = sorted(matches, key=lambda k: k['HammingDistance'])
                if len(matches) > matches_length:
                    matches.pop()
    
    #print the list of matches to the console with name, set and hamming distance
    print("Matches: " + str(len(matches)))
    for match in matches:
        print(f"Name: {match['Card']['Name']} - Set: {match['Card']['Set']['Name']} - Hamming Distance: [{str(match['HammingDistance'])}]")

    # return the best match
    if len(matches) > 0:
        return matches[0]["Card"]
    else:
        return None    

def toHash(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    resized = cv.resize(gray, (16, 16))
    avg = resized.mean()
    hash = (resized > avg).flatten()
    return hash
    
def url_to_image(url) -> np.ndarray | None:
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    # if the image cannot be downloaded, return None
    try:
        resp = urlopen(req)
        img = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv.imdecode(img, cv.IMREAD_COLOR) # The image object
        # return the image
        return img
    except:
        return None