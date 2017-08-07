import json
import urllib2
import os
from multiprocessing import Pool

def download(projectBaseURL):
    projectName = os.path.basename(os.path.normpath(projectBaseURL))
    url = projectBaseURL + "book.json"
    bookJsonData = urllib2.urlopen(url).read()

    print(projectName + ": Starting")

    bookJson = json.loads(bookJsonData)

    if "sampleCode" not in bookJson:
        print(projectName + ": Retired")
        return
    fileName = bookJson["sampleCode"]

    filePath = os.path.join(sampleFolderDirectory, fileName)
    if not os.path.exists(filePath):
        print(projectName+ ": Downloading...")
        with open(filePath,'wb') as f:
            f.write(urllib2.urlopen(projectBaseURL + fileName).read())
            f.close()
    else:
        print(projectName + ": Skipping")

if __name__ == '__main__':

    sampleFolderDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "LegacySamples")
    if not os.path.exists(sampleFolderDirectory):
        os.makedirs(sampleFolderDirectory)

    libraryJsonData = urllib2.urlopen("https://developer.apple.com/library/content/navigation/library.json")

    # Apple's file isn't valid JSON :(
    fixApplesMistake = '{ "items": ' + libraryJsonData.read().split('"documents"')[1][1:]
    libraryJson = json.loads(fixApplesMistake)

    if "items" not in libraryJson:
        raise ValueError("Couldn't get items")

    # item at index 9 is the url, first 2 characters are '..', value at index two for each item is category, 5 = sample code
    baseURL = "https://developer.apple.com/library/content"
    items = [(baseURL + a[9][2:]).split("Introduction")[0] for a in libraryJson["items"] if a[2] == 5]

    print("Downloading " + str(len(items)) + " samples")
    Pool(6).map(download, items)
    print("Done")
