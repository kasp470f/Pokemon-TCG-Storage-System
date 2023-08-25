import asyncio
import json
import threading
import cv2 as cv
import numpy as np
from urllib.request import Request, urlopen
import imagehash
import PIL.Image as Image

# load the file from path dataset/dataset.json
api_dataset = open('data/scraper/api_dataset.json', 'r')

# parse the json file
dataset = json.load(api_dataset)

total = len(dataset)
missingImages = 0
missingCards = []
redoHashes = False
currentIndex = 0

hashSize = 16

async def url_to_image(url):
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

def toStringHash(hashArray):
    return ''.join(['1' if x else '0' for x in hashArray])

def hashDatasetPart(start, end):
    global missingImages, currentIndex
    # loop through the dataset  
    for card in dataset[start:end]:
        # if card is not already hashed, hash it
        try:
            if 'Hash' not in card or redoHashes:
                # load the image
                imgUrl = card['Images']['large']
                # read the image from the link
                img = asyncio.run(url_to_image(imgUrl))
                if img is None:
                    print("Error: " + str(card['Name']) + " image not found.")
                    missingImages = missingImages + 1
                    missingCards.append(card)
                    continue
                else:
                    # save the hash to the dataset
                    card['Hash'] = imagehash.phash(Image.fromarray(img)).__str__()
                    # print in procentage progress
                    print(str(currentIndex) + "/" + str(total - missingImages) + " " + str(round(currentIndex / (total - missingImages) * 100, 2)) + "%")
                    currentIndex = currentIndex + 1
        except Exception as error:
            print("Error: " + str(card['Name']) + " could not be hashed.")
            print(error)

amount = len(dataset)

threads_amount = 10
threads = []
for i in range(0, threads_amount):
    start = int(i * amount / threads_amount)
    end = int((i + 1) * amount / threads_amount)
    _thread = threading.Thread(target=hashDatasetPart, args=(start, end))
    _thread.name = f"Hashing Thread {i} ({start}-{end})"
    threads.append(_thread)
    threads[i].start()


for i in range(0, threads_amount):
    threads[i].join()

# save the dataset as hash_dataset.json in the same directory
with open('data/scraper/hash_dataset.json', 'w') as outfile:
    json.dump(dataset, outfile, indent=4)

# print the number of images that were not found
print("Missing images: " + str(missingImages))

# close the file
api_dataset.close()
