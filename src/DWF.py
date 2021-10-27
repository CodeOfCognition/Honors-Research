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
from analyzeAndGraph import analyze, genHistogram

### File input arguments ###

# #Parse arguments from command line
# parser = argparse.ArgumentParser()
# parser.add_argument('-c', '--corpora_directory')
# parser.add_argument('-v', '--vector_words_file')
# args = parser.parse_args()
# corporaDir = args.corpora_directory
# vectorWordsFile = args.vector_words_file

corporaDir = "/Users/robdow/Desktop/honors research/Coding/data/corpora/DWF_5200_corpora_clean"
vectorWordsFile = "/Users/robdow/Desktop/honors research/Coding/data/vector_words_5200_corpora.txt"

# Gets name of corpus directory (cuts off path leading up to it)
index = corporaDir.rfind("/")
corporaDirName = corporaDir[index + 1:]

start_time = time.time()

def importData(corpus):
    with open(corpus, "rt") as f:
        fin = f.read()
        f.close()
    return fin.split()

def createQuantiles(listedDataSampled):
    check = 0
    uniqueWords = set()
    totalWords = len(listedDataSampled)

    zeros = [0]*150000 # size of WF vector
    dictionary1 = dict(zip(vectorWords, zeros)) 
    dictionary2 = dict(zip(vectorWords, zeros)) 
    dictionary3 = dict(zip(vectorWords, zeros)) 
    dictionary4 = dict(zip(vectorWords, zeros)) 

    for i in range(totalWords):
        uniqueWords.add(listedDataSampled[i])
        if i <= (totalWords//4):
            dictionary1[listedDataSampled[i]] += 1
            check += 1
        elif i <= ((totalWords)//2):
            dictionary2[listedDataSampled[i]] += 1
            check += 1
        elif i <= ((3*totalWords)//4):
            dictionary3[listedDataSampled[i]] += 1
            check += 1
        else:
            dictionary4[listedDataSampled[i]] += 1
            check += 1
    if(len(uniqueWords) < 5000):
        return 0,0,0,0,False
    else:
        return dictionary1, dictionary2, dictionary3, dictionary4, True

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
    cosineValues.append([vc12,vc13,vc14,vc23,vc24,vc34])

def writeResults(cosineValues):
    with open("./data/results/DWF_" + corporaDirName + ".csv", "wt") as f:
        f.write("vc12,vc13,vc14,vc23,vc24,vc34\n")
        for lst in cosineValues:
            for i in range(6):
                if not i == 5:
                    f.write(str(lst[i]) + ",")
                else:
                    f.write(str(lst[i]) + "\n")

def runFile(corpus):

    # Need to import DWF corpora data and list it to proceed

    listedData = importData(corpus)
    results = createQuantiles(listedData)
    dictionary1, dictionary2, dictionary3, dictionary4, usableSample = results[0], results[1], results[2], results[3], results[4]
    if not usableSample:
        return
    processQuantiles(dictionary1, dictionary2, dictionary3, dictionary4)
    subredditString = ""
        

with open(vectorWordsFile, "rt") as f:
    fin = f.read()
    vectorWords = fin.split()
    f.close
cosineValues = list()
i = 1
for filename in os.listdir(corporaDir):
    if filename.endswith(".txt"):
        if (i%10 == 0):
            print(f"--- {round((time.time() - start_time), 2)} seconds ---")
        if (i%10 == 0):
            print(f"running file {i}: {filename}")
        runFile(f"{corporaDir}/{filename}")
        i += 1

writeResults(cosineValues)
analyze(cosineValues)
print(f"Finished in: {round((time.time() - start_time), 2)} seconds")
print(f"DWF analysis complete after {len(cosineValues)} trials ran.\nPlease copy the results printed above of average cosine values and standard errors.\nA copy of the resulting cosine values for each trial are printed in data/results/IUWF_(nameOfCorporaDirectory).csv")
genHistogram(cosineValues, "DWF", .5, 1, 0, .16)