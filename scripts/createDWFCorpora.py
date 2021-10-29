import re
import numpy as np
import pandas as pd
import nltk
from scipy import spatial
import random
import os
import math
import time
import matplotlib.pyplot as plt
import argparse

def loadVectorWords(vectorWordsFile):
    with open(vectorWordsFile, "rt") as f:
        fin = f.read()
        f.close
    vectorWords = set(fin.split())
    return vectorWords

def importData(corpus):
    df = pd.read_csv(corpus, header=None)
    df.columns = ["time", "subreddit", "wordcount", "comment"]
    df = df.sort_values(['subreddit', 'time'], ascending=(True, True)).reset_index()
    return df

def findUsableDiscourseRanges(df):
    wcs = list()
    rangeStart=0
    wc = 0
    threshold = 100000
    currentSubreddit = df['subreddit'][0]

    validRanges = list() #includes lists of ranges with word counts of 100000+
    for index, row in df.iterrows():
        if (currentSubreddit == df['subreddit'][index]): #same subreddit
            wc += int(df['wordcount'][index])
        elif (wc < threshold): #new subreddit, last subreddit was below threshold
            currentSubreddit = df['subreddit'][index]
            rangeStart=index
            wc = int(df['wordcount'][index])
        else: #new subreddit, last subreddit was above threshold
            currentSubreddit = df['subreddit'][index]
            validRanges.append([rangeStart, index-1])
            rangeStart=index
            wc = int(df['wordcount'][index])
    if wc>threshold: #handles last comment
        validRanges.append([rangeStart,len(df["wordcount"])-1]) # CHECK this line
    return validRanges

def getRandomSamples(validRanges, df):
    listedData = list()
    subredditString = ""
    j=0
    # cycle through comments from single discourses for each valid range
    for i in range(len(validRanges)):
        # put all comments into one string
        for j in range(validRanges[i][0],validRanges[i][1]):
            subredditString += str(df['comment'][j])
        listedData = subredditString.split(' ')[0:-1]
    
    totalWords = len(listedData)
    if(totalWords>100000):
        numToRemove = totalWords - 100000
        toRemove = random.sample(range(totalWords), numToRemove)
        toRemove.sort(reverse=True)
        for i in toRemove:
            listedData.pop(i)
    
    # if not totalWords == 100000:
    #     print("error - word length wrong with " + str(totalWords) + "words")
    return listedData

def writeNewCorpora(listedData, corpus, corporaDirName, df, validRanges):
        subredditString = " ".join(listedData)
        index = corpus.rfind("/")
        corpusName = corpus[index + 1:-4]
        for i in range(len(validRanges)):
            with open(f"./data/corpora/DWF_{corporaDirName}/{df['subreddit'][validRanges[i][0]]}_{corpusName}.txt", "wt") as f:
                f.write(subredditString)
                f.close()

        subredditString = ""

def runFile(corpus, corporaDirName):

    df = importData(corpus)
    validRanges  = findUsableDiscourseRanges(df)
    listedData = getRandomSamples(validRanges, df)
    writeNewCorpora(listedData, corpus, corporaDirName, df, validRanges)

def main(corporaDir, vectorWordsFile):
    # Gets name of corpus directory (cuts off path leading up to it)
    index = corporaDir.rfind("/")
    corporaDirName = corporaDir[index + 1:]

    if not os.path.isdir(f"./data/corpora/DWF_{corporaDirName}"):
        os.mkdir(f"./data/corpora/DWF_{corporaDirName}")

    vectorWords = loadVectorWords(vectorWordsFile)
    cosineValues = list()
    i = 1
    for filename in os.listdir(corporaDir):
        if filename.endswith(".csv"):
            if (i%10 == 0):
                print(f"--- {round((time.time() - start_time), 2)} seconds ---")
            if (i%10 == 0):
                print(f"running file {i}: {filename}")
            runFile(f"{corporaDir}/{filename}", corporaDirName)
            i += 1
    print(f"createDWFCorpora.py finished running in {round((time.time() - start_time), 2)} seconds.")

if __name__ == "__main__":
    
    start_time = time.time()

    print("Running script: createDWFCorpora.py")
    # #Parse arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--corpora_directory')
    parser.add_argument('-v', '--vector_words_file')
    args = parser.parse_args()
    corporaDir = args.corpora_directory
    vectorWordsFile = args.vector_words_file

    # corporaDir = "/Users/robdow/Desktop/honors research/Coding/data/corpora/10_corpora_clean"
    # vectorWordsFile = "/Users/robdow/Desktop/honors research/Coding/data/vector_words_10_corpora.txt"
    
    main(corporaDir, vectorWordsFile)