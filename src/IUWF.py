import os
import re
import numpy as np
import pandas as pd
from scipy import spatial
import math
import os
import json
import time
import matplotlib.pyplot as plt
import random

global badUsers 
badUsers = list()
start_time = time.time()

def runFile(corpus, vectorWordsFile, numTrainWords, takeLog, runControl):
    dfData = pd.read_csv(corpus, header=None)
    dfData.columns = ["time", "subreddit", "wc", "comment"]
    if not runControl:
        dfData = dfData.sort_values('time', ascending=(True)).reset_index()
    else:
        dfData = dfData.sample(frac=1)

    with open(vectorWordsFile, "rt") as f:
        fin = f.read()
        train_words = fin.split()
        f.close

    zeros = [0]*numTrainWords # size of WF vector
    dictionary1 = dict(zip(train_words, zeros)) 
    dictionary2 = dict(zip(train_words, zeros)) 
    dictionary3 = dict(zip(train_words, zeros)) 
    dictionary4 = dict(zip(train_words, zeros)) 

    listedData = (dfData['comment'].str.cat(sep=''))
    listedData = listedData.split(' ')[:-1]
    totalWords = len(listedData)

    toAdd = random.sample(range(totalWords), 100000)
    toAdd.sort()
    newListedData = list()
    for i in toAdd:
        newListedData.append(listedData[i])
    totalWords = len(newListedData)
    if not totalWords == 100000:
        print("error - word length wrong with " + str(totalWords) + "words")


    check = 0
    uniqueWords = set()

    for i in range(totalWords):
        uniqueWords.add(listedData[i])
        if i <= (totalWords//4):
            dictionary1[listedData[i]] += 1
            check += 1
        elif i <= ((totalWords)//2):
            dictionary2[listedData[i]] += 1
            check += 1
        elif i <= ((3*totalWords)//4):
            dictionary3[listedData[i]] += 1
            check += 1
        else:
            dictionary4[listedData[i]] += 1
            check += 1
    if(len(uniqueWords) < 5000):
        badUsers.append(corpus[:-4])
        return

    
    f1 = list(dictionary1.values())
    f2 = list(dictionary2.values())
    f3 = list(dictionary3.values())
    f4 = list(dictionary4.values())
    
    if takeLog:
        temp = list()
        for value in f1:
            if value != 0:
                temp.append(math.log10(value))
            else:
                temp.append(0)
        f1 = temp
        temp = list()
        for value in f2:
            if value != 0:
                temp.append(math.log10(value))
            else:
                temp.append(0)
        f2 = temp
        temp = list()
        for value in f3:
            if value != 0:
                temp.append(math.log10(value))
            else:
                temp.append(0)
        f3 = temp
        temp = list()
        for value in f4:
            if value != 0:
                temp.append(math.log10(value))
            else:
                temp.append(0)
        f4 = temp

    vc12 = 1-spatial.distance.cosine(f1, f2)
    vc13 = 1-spatial.distance.cosine(f1, f3)
    vc14 = 1-spatial.distance.cosine(f1, f4)
    vc23 = 1-spatial.distance.cosine(f2, f3)
    vc24 = 1-spatial.distance.cosine(f2, f4)
    vc34 = 1-spatial.distance.cosine(f3, f4)
    cosineValues.append([vc12,vc13,vc14,vc23,vc24,vc34])

def run(prePath, corporaDir, vectorWordsFile, numVectorWords, takeLog, runControl):

    randomFileIndexList = random.sample(range(5201), 2825)
    randomFileIndexList.sort()
    unusedFiles = list()
    i = 1
    j = 1
    for filename in os.listdir(prePath + corporaDir):
        if i in randomFileIndexList:
            if filename.endswith(".csv"):
                if (j%25 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                if (j%25 == 0):
                    print("running file " + str(j) + " of " + str(i) + ": " + filename)
                    print("Bad User Count: " + str(len(badUsers)))
                runFile(((prePath + corporaDir + '/' + filename)), vectorWordsFile, numVectorWords, takeLog, runControl)
                j += 1
        else:
            unusedFiles.append(filename)
        i += 1

    i = 0
    randomExtraIndexes = random.sample(range(len(unusedFiles)), len(unusedFiles))
    for j in randomExtraIndexes:
        if (len(badUsers) - i) == 0:
            break
        else:
            runFile(((prePath + corporaDir + '/' + unusedFiles[j])), vectorWordsFile, numVectorWords, takeLog, runControl)
            i += 1

    # analyze(cosineValues)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(corporaDir + "\t" + str(vectorWordsFile) + "\t" + str(numVectorWords))



cosineValues = list()
run('/Volumes/Robbie_External_Hard_Drive/', '5200_corpora_clean', './helperFiles/vector_words_150000_derived_5200_corpora.txt', 150000, False, False)
print("Bad Users: " + str(len(badUsers)) + "\n" + str(badUsers))
# genHistogram("5200")
