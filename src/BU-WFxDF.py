import numpy as np
import pandas as pd
from scipy import spatial
import math
import json
import time
import matplotlib.pyplot as plt
import random
import csv
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

def loadVectorWords(vectorFile):

    with open(vectorFile, "rt") as f:
        fin = f.read()
        vectorWords = fin.split()
        f.close
    return vectorWords

def loadUserDiscourseVectors(corporaDirName):

    with open(os.path.join(parentdir, "data", f"discourseFrequencies_{corporaDirName}.json"), "rt") as f:
        discourseVectors = json.load(f)
        f.close()

    return discourseVectors

def selectTwoCorpora(i, setOfUsedPairs, corpusList):

    i2 = -1
    while ((i, i2) in setOfUsedPairs) or ((i2, i) in setOfUsedPairs) or (i2 == -1) or (i2 == i):
        i2 = random.randint(0, len(corpusList)-1)
    setOfUsedPairs.add((i, i2))
    return setOfUsedPairs, corpusList[i], corpusList[i2]

def getDiscourseFrequency(corpus1, corpus2, discFreqBins, dictOfDiscourseVectors, binSize, aveDiscsPerBin):

    vector1 = dictOfDiscourseVectors[corpus1]
    vector2 = dictOfDiscourseVectors[corpus2]
    numDiscs1 = len(set(vector1)) - 1 # calculates number of discourses contributed to
    numDiscs2 = len(set(vector2)) - 1 # calculates number of discourses contributed to
    dfVC = 1-spatial.distance.cosine(vector1, vector2) #discourse frequency vector cosine
    if dfVC < 0.1:
        if discFreqBins[0] < binSize:
            discFreqBins[0] += 1
            aveDiscsPerBin[0] = aveDiscsPerBin[0] + numDiscs1 + numDiscs2
            return discFreqBins, aveDiscsPerBin, dfVC, True
        else:
            return discFreqBins, aveDiscsPerBin, dfVC, False
    elif dfVC < 0.2:
        if discFreqBins[1] < binSize:
            discFreqBins[1] += 1
            aveDiscsPerBin[1] = aveDiscsPerBin[1] + numDiscs1 + numDiscs2
            return discFreqBins, aveDiscsPerBin, dfVC, True
        else:
            return discFreqBins, aveDiscsPerBin, dfVC, False
    elif dfVC < 0.3:
        if discFreqBins[2] < binSize:
            discFreqBins[2] += 1
            aveDiscsPerBin[2] = aveDiscsPerBin[2] + numDiscs1 + numDiscs2
            return discFreqBins, aveDiscsPerBin, dfVC, True
        else:
            return discFreqBins, aveDiscsPerBin, dfVC, False
    elif dfVC < 0.4:
        if discFreqBins[3] < binSize:
            discFreqBins[3] += 1
            aveDiscsPerBin[3] = aveDiscsPerBin[3] + numDiscs1 + numDiscs2
            return discFreqBins, aveDiscsPerBin, dfVC, True
        else:
            return discFreqBins, aveDiscsPerBin, dfVC, False
    elif dfVC < 0.5:
        if discFreqBins[4] < binSize:
            discFreqBins[4] += 1
            aveDiscsPerBin[4] = aveDiscsPerBin[4] + numDiscs1 + numDiscs2
            return discFreqBins, aveDiscsPerBin, dfVC, True
        else:
            return discFreqBins, aveDiscsPerBin, dfVC, False
    elif dfVC < 0.6:
        if discFreqBins[5] < binSize:
            discFreqBins[5] += 1
            aveDiscsPerBin[5] = aveDiscsPerBin[5] + numDiscs1 + numDiscs2
            return discFreqBins, aveDiscsPerBin, dfVC, True
        else:
            return discFreqBins, aveDiscsPerBin, dfVC, False
    elif dfVC < 0.7:
        if discFreqBins[6] < binSize:
            discFreqBins[6] += 1
            aveDiscsPerBin[6] = aveDiscsPerBin[6] + numDiscs1 + numDiscs2
            return discFreqBins, aveDiscsPerBin, dfVC, True
        else:
            return discFreqBins, aveDiscsPerBin, dfVC, False
    elif dfVC < 0.8:
        if discFreqBins[7] < binSize:
            discFreqBins[7] += 1
            aveDiscsPerBin[7] = aveDiscsPerBin[7] + numDiscs1 + numDiscs2
            return discFreqBins, aveDiscsPerBin, dfVC, True
        else:
            return discFreqBins, aveDiscsPerBin, dfVC, False
    elif dfVC < 0.9:
        if discFreqBins[8] < binSize:
            discFreqBins[8] += 1
            aveDiscsPerBin[8] = aveDiscsPerBin[8] + numDiscs1 + numDiscs2
            return discFreqBins, aveDiscsPerBin, dfVC, True
        else:
            return discFreqBins, aveDiscsPerBin, dfVC, False
    else:
        if discFreqBins[9] < binSize:
            discFreqBins[9] += 1
            aveDiscsPerBin[9] = aveDiscsPerBin[9] + numDiscs1 + numDiscs2
            return discFreqBins, aveDiscsPerBin, dfVC, True
        else:
            return discFreqBins, aveDiscsPerBin, dfVC, False
 

def getWordFrequency(corpus1, corpus2, vectorWords, corporaDir):

    wfDataFrame1 = pd.read_csv(os.path.join(corporaDir, corpus1), header=None)
    wfDataFrame1.columns = ["time", "subreddit", "wc", "comment"]
    wfDataFrame2 = pd.read_csv(os.path.join(corporaDir, corpus2), header=None)
    wfDataFrame2.columns = ["time", "subreddit", "wc", "comment"]

    zeros = [0]*150000 
    dictionary1 = dict(zip(vectorWords, zeros))
    dictionary2 = dict(zip(vectorWords, zeros)) 

    wordData1 = (wfDataFrame1['comment'].str.cat(sep=' ').split())
    wordData2 = (wfDataFrame2['comment'].str.cat(sep=' ').split())

    for word in wordData1:
        dictionary1[word] += 1
    for word in wordData2:
        dictionary2[word] += 1
    
    wordVector1 = list(dictionary1.values())
    wordVector2 = list(dictionary2.values())

    wfVC = 1-spatial.distance.cosine(wordVector1, wordVector2) #word frequency vector cosine
    return wfVC

def runFile(i, corporaDir, corpusList, setOfUsedPairs, vectorWords, dictOfDiscourseVectors, discFreqBins, binSize, aveDiscsPerBin):

    setOfUsedPairs, corpus1, corpus2 = selectTwoCorpora(i, setOfUsedPairs, corpusList)
    discFreqBins, aveDiscsPerBin, dfVC, isUsable = getDiscourseFrequency(corpus1, corpus2, discFreqBins, dictOfDiscourseVectors, binSize, aveDiscsPerBin)
    if not isUsable:
        return 0,0,discFreqBins,aveDiscsPerBin, setOfUsedPairs,False
    wfVC = getWordFrequency(corpus1, corpus2, vectorWords, corporaDir)
    return wfVC, dfVC, discFreqBins, aveDiscsPerBin, setOfUsedPairs, isUsable

def exportResults(dfwfPairs, corporaDirName):
    with open(os.path.join(parentdir, "data", "results", f"wf_df_{corporaDirName}_v2.csv"), "wt") as f:
        writer = csv.writer(f)
        writer.writerow(["df similarity", "wf similarity"])
        for pair in dfwfPairs:
            writer.writerow([pair[0], pair[1]])

def main(corporaDir, vectorWordsFile, binSize):

    # Gets name of corpus directory (cuts off path leading up to it)
    index = corporaDir.rfind("/")
    corporaDirName = corporaDir[index + 1:]

    vectorWords = loadVectorWords(vectorWordsFile)
    dictOfDiscourseVectors = loadUserDiscourseVectors(corporaDirName)
    setOfUsedPairs = set()
    discFreqBins = [0,0,0,0,0,0,0,0,0,0] # holds the number of processed discourse frequency across range of possible similarity values (0.0-0.1, 0.1-0.2, ... 0.9-1.0)
    aveDiscsPerBin = [0,0,0,0,0,0,0,0,0,0] # holds average discourses per bin. First aggregated, then averaged by dividing each bin by size.

    #gets list of corpus file names
    dirContents = os.listdir(corporaDir)
    corpusList = list()
    for file in dirContents:
        if file.endswith(".csv"):
            corpusList.append(file)

     # The code below continually calls runFile() until all bins are filled. It also prints progress updates to the standard out.

    dfwfPairs = list()
    toPrint = True #controls whether or not to print bin contents
    c = 1 # keeps track of how many cycles through all corpora have occurred (current iteration)
    # iterate through all corpora continually until all bins are full
    while (discFreqBins[0] + discFreqBins[1] + discFreqBins[2] + discFreqBins[3] + discFreqBins[4] + discFreqBins[5] + discFreqBins[6] + discFreqBins[7] + discFreqBins[8] + discFreqBins[9] < (10*binSize)):
        for i in range(len(corpusList)):
            if i == 0:
                print(f"Cycle {c}")
            if toPrint and ((discFreqBins[0] + discFreqBins[1] + discFreqBins[2] + discFreqBins[3] + discFreqBins[4] + discFreqBins[5] + discFreqBins[6] + discFreqBins[7] + discFreqBins[8] + discFreqBins[9]) % 5 == 0):
                print(f"--- {round((time.time() - start_time), 2)} seconds ---")
                print(f"Bins: [ {discFreqBins[0]} {discFreqBins[1]} {discFreqBins[2]} {discFreqBins[3]} {discFreqBins[4]} {discFreqBins[5]} {discFreqBins[6]} {discFreqBins[7]} {discFreqBins[8]} {discFreqBins[9]} ] (bin capactiy: {binSize})")
            results = runFile(i, corporaDir, corpusList, setOfUsedPairs, vectorWords, dictOfDiscourseVectors, discFreqBins, binSize, aveDiscsPerBin)
            wfVC, dfVC, discFreqBins, aveDiscsPerBin, setOfUsedPairs, isUsable = results[0], results[1], results[2], results[3], results[4], results[5]
            if isUsable:
                dfwfPairs.append((dfVC, wfVC))
                toPrint = True # allows new results to print
            else:
                toPrint = False # blocks printing same results

            if (discFreqBins[0] + discFreqBins[1] + discFreqBins[2] + discFreqBins[3] + discFreqBins[4] + discFreqBins[5] + discFreqBins[6] + discFreqBins[7] + discFreqBins[8] + discFreqBins[9]) == (10*binSize):
                break
        c += 1
    
    finalBinAves = list()
    for b in aveDiscsPerBin:
        finalBinAves.append(b/(binSize*2))
    print(f"Average discourses used per bin: {finalBinAves}")
    exportResults(dfwfPairs, corporaDirName)
    print(f"WFxDF.py finished running in {round((time.time() - start_time), 2)} seconds. Results are written to the data/results directory.")
        
    

if __name__ == "__main__":

    start_time = time.time()
    print("Running model: BU-WFxDF.py")

    # # Parse arguments from command line
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-c', '--corpora_directory') #expects cleaned corpora 
    # parser.add_argument('-vw', '--vector_words_file') 
    # parser.add_argument('-b', '--bin_size') 
    # args = parser.parse_args()
    # corporaDir = args.corpora_directory
    # vectorDiscoursesFile = args.vector_discourses_file
    # vectorWordsFile = args.vector_words_file
    # binSize = args.binSize

    corporaDir = os.path.join(parentdir, "data", "corpora", "5200_corpora_clean")
    vectorWordsFile = os.path.join(parentdir, "data", "vector_words_5200_corpora.txt")
    binSize = 2000
    
    main(corporaDir, vectorWordsFile, binSize)