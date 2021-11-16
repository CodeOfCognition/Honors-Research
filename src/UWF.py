import os
import re
import numpy as np
import pandas as pd
from scipy import spatial
import math
import os
import time
import matplotlib.pyplot as plt
import random
import argparse
from analyzeAndGraph import analyze, genHistogram

def loadVectorWords(vectorWordsFile):
    with open(vectorWordsFile, "rt") as f:
        fin = f.read()
        vectorWords = fin.split()
        f.close
    return vectorWords

def importData(corpus, runControl):
    df = pd.read_csv(corpus, header=None)
    df.columns = ["time", "subreddit", "wc", "comment"]
    if not runControl:
        df = df.sort_values('time', ascending=(True)).reset_index()
    else:
        df = df.sample(frac=1)
    # df_len = len(df["time"])
    # df = df.iloc[(2*(df_len//3)):(df_len - 1)]
    # df_len = len(df["time"])
    return df

def getRandomSamples(df, vectorWords):
    listedData = (df['comment'].str.cat(sep=''))
    listedData = listedData.split(' ')[:-1]
    totalWords = len(listedData)

    try:
        toAdd = random.sample(range(totalWords), 100000)
    except ValueError: # occurs if corpus has <100,000 words which shouldn't happen in the standard implementation with 5200 corpora. This was used mostly for other testing
        return []
    toAdd.sort()
    newListedData = list()
    for i in toAdd:
        newListedData.append(listedData[i])

    return newListedData

def createQuantiles(vectorWords, listedData, corpus):

    zeros = [0]*150000 # size of WF vector
    dictionary1 = dict(zip(vectorWords, zeros)) 
    dictionary2 = dict(zip(vectorWords, zeros)) 
    dictionary3 = dict(zip(vectorWords, zeros)) 
    dictionary4 = dict(zip(vectorWords, zeros)) 

    totalWords = len(listedData)
    check = 0
    uniqueWords = set()

    for i in range(totalWords):
        uniqueWords.add(str(listedData[i]))
        if i <= (totalWords//4):
            dictionary1[str(listedData[i])] += 1
            check += 1
        elif i <= ((totalWords)//2):
            dictionary2[str(listedData[i])] += 1
            check += 1
        elif i <= ((3*totalWords)//4):
            dictionary3[str(listedData[i])] += 1
            check += 1
        else:
            dictionary4[str(listedData[i])] += 1
            check += 1
    if(len(uniqueWords) < 5000):
        return 0,0,0,0,-1 # indicates corpus quantiles were not created
    return dictionary1, dictionary2, dictionary3, dictionary4, 1

def processQuantiles(dictionary1, dictionary2, dictionary3, dictionary4):
    f1 = list(dictionary1.values())
    f2 = list(dictionary2.values())
    f3 = list(dictionary3.values())
    f4 = list(dictionary4.values())

    vc12 = 1-spatial.distance.cosine(f1, f2)
    vc13 = 1-spatial.distance.cosine(f1, f3)
    vc14 = 1-spatial.distance.cosine(f1, f4)
    vc23 = 1-spatial.distance.cosine(f2, f3)
    vc24 = 1-spatial.distance.cosine(f2, f4)
    vc34 = 1-spatial.distance.cosine(f3, f4)
    return [vc12,vc13,vc14,vc23,vc24,vc34]

def writeResults(cosineValues):
    # Gets name of corpus directory (cuts off path leading up to it)
    index = corporaDir.rfind("/")
    corporaDirName = corporaDir[index + 1:]
    
    with open("./data/results/UWF_" + corporaDirName + ".csv", "wt") as f:
        f.write("vc12,vc13,vc14,vc23,vc24,vc34\n")
        for lst in cosineValues:
            for i in range(6):
                if not i == 5:
                    f.write(str(lst[i]) + ",")
                else:
                    f.write(str(lst[i]) + "\n")

def runFile(corpus, vectorWords, runControl):

    df = importData(corpus, runControl)

    listedData = getRandomSamples(df, vectorWords) #gets 100,000 randomly sampled words
    if listedData == []:
        return 0, []

    results = createQuantiles(vectorWords, listedData, corpus)
    if results[4] == -1:
        return 0, [] #unusable corpus

    dictionary1, dictionary2, dictionary3, dictionary4 = results[0], results[1], results[2], results[3]
    cosineValue = processQuantiles(dictionary1, dictionary2, dictionary3, dictionary4)

    return 1, cosineValue

def runNFiles(corporaDir, vectorWords, runControl, n):
    cosineValues = list()
    randomFileIndexList = random.sample(range(5200), 5200)
    fileNames = list()
    for filename in os.listdir(corporaDir):
        fileNames.append(filename)
    i = 1
    for fileIndex in randomFileIndexList:
        if (i%25 == 0):
            print(f"--- {round((time.time() - start_time), 2)} seconds ---")
            print(f"running file {i}: {fileNames[fileIndex]}")
        results = runFile(((corporaDir + '/' + fileNames[fileIndex])), vectorWords, runControl)
        i += results[0]
        if results[0] == 1:
            cosineValues.append(results[1])
        if i > n:
            return cosineValues
    return cosineValues

def main(corporaDir, vectorWordsFile, runControl, n):

    vectorWords = loadVectorWords(vectorWordsFile)
    cosineValues = runNFiles(corporaDir, vectorWords, runControl, n) 
    writeResults(cosineValues)
    analyze(cosineValues)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(f"UWF analysis complete after {len(cosineValues)} trials ran.\nPlease copy the results printed above of average cosine values and standard errors.\nA copy of the resulting cosine values for each trial are printed in data/results/UWF_(nameOfCorporaDirectory).csv")

    genHistogram(cosineValues, "UWF", 0.5, 1, 0, 0.175)
    

if __name__ == "__main__":
    # #Parse arguments from command line
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-c', '--corpora_directory')
    # parser.add_argument('-v', '--vector_words_file')
    # parser.add_argument('-n', '--number_of_trials')
    # parser.add_argument('-control', '--true_or_false') #must be 0 for false, or 1 for true
    # args = parser.parse_args()
    # corporaDir = args.corpora_directory
    # vectorWordsFile = args.vector_words_file
    # runControl = int(args.true_or_false)
    # n = args.number_of_files

    corporaDir = "/Users/robdow/Desktop/honors research/Coding/data/corpora/5200_corpora_clean"
    vectorWordsFile = "/Users/robdow/Desktop/honors research/Coding/data/vector_words_5200_corpora.txt"
    runControl = False
    n = 2825

    start_time = time.time()

    main(corporaDir, vectorWordsFile, runControl, n)