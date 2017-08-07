import json
import urllib2
import os
import time
from bs4 import BeautifulSoup

from multiprocessing import Pool

def fetchVideoResources(videoURL):
    videoID = os.path.basename(os.path.normpath(videoURL))
    print(videoID + ": Starting")

    videoPage = urllib2.urlopen(videoURL).read()
    videoSoup = BeautifulSoup(videoPage, "html.parser")
    videoResources = videoSoup.findAll("a", { "target" : "_blank" })
    videoResources = [a["href"] for a in videoResources if ".zip" in a["href"]]

    if len(videoResources) == 0:
        print(videoID + ": No zips")
    else:
        print(videoID + ": Zips: " + str(len(videoResources)))

    for resouce in videoResources:
        fileName = os.path.basename(os.path.normpath(resouce))
        filePath = os.path.join(sampleFolderDirectory, fileName)
        if not os.path.exists(filePath):
            print(videoID + ": Downloading zip...")
            with open(filePath,'wb') as f:
                f.write(urllib2.urlopen(resouce).read())
                f.close()
        else:
            print(videoID + ": Skipping zip")

if __name__ == '__main__':

    sampleFolderDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "WWDC17Samples")
    if not os.path.exists(sampleFolderDirectory):
        os.makedirs(sampleFolderDirectory)

    frameworks = urllib2.urlopen('https://developer.apple.com/videos/wwdc2017/').read()

    soup = BeautifulSoup(frameworks, "html.parser")
    videoLinks = soup.find_all('a', href=True)

    videoLinks = ["https://developer.apple.com/" + a["href"] for a in videoLinks if "/videos/play/wwdc" in a["href"]]
    videoLinks = list(set(videoLinks))

    print("Searching " + str(len(videoLinks)) + " videos for session samples")
    Pool(6).map(fetchVideoResources, videoLinks)
    print("Done")
