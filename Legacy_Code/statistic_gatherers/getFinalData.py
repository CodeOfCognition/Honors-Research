import os
import re
import csv
import time
import math
import pandas as pd
import argparse



def extractCorpusInformation(corporaDir, filename):
    with open(corporaDir + "/" + filename, "rt") as f:
        fin = f.read()
        f.close

        entry_pat = "\*--\s(.*?)--\*" # Separates entries
        subreddit_pat = '\d\d\d\d\d\d\d\d\d\d\s(.*?)\s' # what comes after 10 digit pattern in first line
        comment_pat = '\n(.*)' # what comes after the first line
        
        entries = re.findall(entry_pat, fin, re.DOTALL)

        subreddits = list()
        rawComments = list()

        numEntries = len(entries)
        j = 0
        for i in range(numEntries):
            try:
                subreddit = re.search(subreddit_pat, entries[i]).group(1)
                rawComment = re.search(comment_pat, entries[i], re.DOTALL).group(1)
            except: # Handles malformed entries
                continue
            subreddits.append(subreddit)
            rawComments.append(rawComment)
            j += 1
        return subreddits, rawComments


def runFile(filename):
    
    corpusInfo = extractCorpusInformation(corporaDir, filename)
    subreddits, rawComments = corpusInfo[0], corpusInfo[1]
    nSubs = len(set(subreddits))
    nWords = 0

    for i in range(len(rawComments)):
        nWords += len(rawComments[i].split())
    nWordsComment = nWords / i

    return nSubs, nWords, nWordsComment
    


def main(corporaDir):

    totalSubs = 0
    totalWords = 0
    totalWordsComment = 0


    i = 1 
    for filename in os.listdir(corporaDir):
        if filename.endswith(".txt"):
            if (i%10 == 0):
                print(f"--- {round((time.time() - start_time), 2)} seconds ---")
                print ("Running file " + str(i) + ": " + filename)
            nSubs, nWords, nWordsComment = runFile(filename)
            # print(f"{i}\tnSubs: {nSubs}, nWords: {nWords}, nWordsComment: {nWordsComment}")
            totalSubs += nSubs
            totalWords += nWords
            totalWordsComment += nWordsComment
            i += 1
    i = i - 1
    
    totalWords = totalWords / i
    totalSubs = totalSubs / i
    totalWordsComment = totalWordsComment / i

    with open("paperInfo2.txt", "wt") as f:
        f.write(f"Average Discourses: {totalSubs}\n")
        f.write(f"Average Words: {totalWords}\n")
        f.write(f"Average Comment Length: {totalWordsComment}")

    print(f"cleanCorpora.py finished running in {round((time.time() - start_time), 2)} seconds.")



if __name__ == "__main__":

    start_time = time.time()
    print("Running getFinalData.py")

    corporaDir = "/Volumes/Robbie_External_Hard_Drive/5200_corpora"

    main(corporaDir)