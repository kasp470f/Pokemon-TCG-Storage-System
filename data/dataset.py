import json
import math
from urllib.request import Request, urlopen;
import cv2 as cv;
import numpy as np
import imagehash
import PIL.Image as Image
from PIL import ImageEnhance

from models.card import CardClass;

hamming_distance_threshold = 10;
matches_length = 5;

read_dataset = open('data/hash_dataset.json', 'r')

# parse the json file
dataset: list[CardClass] = json.load(read_dataset)

def findMatch(image: np.ndarray) -> CardClass | None:
    hash = hashing_class(image)

    matches = []
    # loop through the dataset
    for card in dataset:
        # find the hamming distance between the hash and the card's hash if it exists
        if 'Hash' in card:
            card_hash = imagehash.hex_to_hash(card['Hash'])
            hm = hash.hamming_distance(card_hash)
            # keep only the best matches (lowest hamming distance) in the matches array if a match is found with a hamming distance lower than the threshold and it has a lower hamming distance than the last card in the list then push it to the list in the correct position (sorted by hamming distance) and remove the last card in the list
            if hm < hamming_distance_threshold and (len(matches) < matches_length or hm < matches[-1]['HammingDistance']):
                matches.append({ "HammingDistance": hm, "Card": card})
                matches = sorted(matches, key=lambda k: k['HammingDistance'])
                if len(matches) > matches_length:
                    matches.pop()
    
    #print the list of matches to the console with name, set and hamming distance
    print("Matches: " + str(len(matches)))
    for match in matches:
        print(f"Name: {match['Card']['Name']} - Set: {match['Card']['Set']['Name']}] - Hamming Distance: {round(match['HammingDistance'], 2)}")

    # return the best match
    if len(matches) > 0:
        return matches[0]["Card"]
    else:
        return None    
    
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
    
class hashing_class:
    normal: imagehash.ImageHash;
    lighter_list: list[imagehash.ImageHash];
    darker_list: list[imagehash.ImageHash];

    iterations: int = 5;
    incremental_increase_light: int = 10;
    incremental_increase_dark: int = 5;

    best_lighter: float;
    best_darker: float;
    normal_value: float;

    def __init__(self, image: np.ndarray):
        self.normal = imagehash.dhash(Image.fromarray(image))
        self.lighter_list = []
        self.darker_list = []
        self.hashing_light(image);
        self.hashing_dark(image);

    def hashing_light(self, image: np.ndarray):
        for i in range(1, self.iterations):
            hash_lighter = imagehash.dhash(Image.fromarray(cv.addWeighted(image, 1 + (i * self.incremental_increase_light)/100, image, 0, 0)))
            self.lighter_list.append(hash_lighter)

    def hashing_dark(self, image: np.ndarray):
        for i in range(1, self.iterations):
            hash_darker = imagehash.dhash(Image.fromarray(cv.addWeighted(image, 1, image, 0, (i * self.incremental_increase_dark))))
            self.darker_list.append(hash_darker)

    def hamming_distance(self, card_hash: imagehash.ImageHash) -> float:
        lighter_distances = []
        darker_distances = []

        for lighter in self.lighter_list:
            lighter_distances.append(card_hash - lighter)

        for darker in self.darker_list:
            darker_distances.append(card_hash - darker)

        self.best_lighter = sum(lighter_distances) / len(lighter_distances)
        self.best_darker = sum(darker_distances) / len(darker_distances)
        self.normal_value = self.normal - card_hash

        return sum([self.best_lighter, self.best_darker, self.normal_value]) / 3






    
