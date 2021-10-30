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

def loadVectorWords(vectorWordsFile):
    with open(vectorWordsFile, "rt") as f:
        fin = f.read()
        vectorWords = fin.split()
        f.close
    return vectorWords

def importData(corpus):
    with open(corpus, "rt") as f:
        fin = f.read()
        f.close()
    return fin.split()

def createQuantiles(listedData, vectorWords):
    check = 0
    uniqueWords = set()
    totalWords = len(listedData)

    zeros = [0]*150000 # size of WF vector
    dictionary1 = dict(zip(vectorWords, zeros)) 
    dictionary2 = dict(zip(vectorWords, zeros)) 
    dictionary3 = dict(zip(vectorWords, zeros)) 
    dictionary4 = dict(zip(vectorWords, zeros)) 

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
    return [vc12,vc13,vc14,vc23,vc24,vc34]

def writeResults(cosineValues, corporaDir):
    # Gets name of corpus directory (cuts off path leading up to it)
    index = corporaDir.rfind("/")
    corporaDirName = corporaDir[index + 1:]

    with open("./data/results/" + corporaDirName + ".csv", "wt") as f:
        f.write("vc12,vc13,vc14,vc23,vc24,vc34\n")
        for lst in cosineValues:
            for i in range(6):
                if not i == 5:
                    f.write(str(lst[i]) + ",")
                else:
                    f.write(str(lst[i]) + "\n")

def runFile(corpus, vectorWords):
    listedData = importData(corpus)
    results = createQuantiles(listedData, vectorWords)
    dictionary1, dictionary2, dictionary3, dictionary4, usableSample = results[0], results[1], results[2], results[3], results[4]
    if not usableSample:
        return
    return processQuantiles(dictionary1, dictionary2, dictionary3, dictionary4)
        
def main(corporaDir, vectorWordsFile):

    vectorWords = loadVectorWords(vectorWordsFile)
    cosineValues = list()
    i = 1
    for filename in os.listdir(corporaDir):
        if i == 40:
            break
        if filename.endswith(".txt"):
            if (i%10 == 0):
                print(f"--- {round((time.time() - start_time), 2)} seconds ---")
            if (i%10 == 0):
                print(f"running file {i}: {filename}")
            cosineValue = runFile(f"{corporaDir}/{filename}", vectorWords)
            if not cosineValue == None:
                cosineValues.append(cosineValue)
            i += 1

    writeResults(cosineValues, corporaDir)
    analyze(cosineValues)
    print(f"Finished in: {round((time.time() - start_time), 2)} seconds")
    print(f"DWF analysis complete after {len(cosineValues)} trials ran.\nPlease copy the results printed above of average cosine values and standard errors.\nA copy of the resulting cosine values for each trial are printed in data/results/(nameOfCorporaDirectory).csv")
    genHistogram(cosineValues, "DWF", .5, 1, 0, .16)

if __name__ == "__main__":
    ### File input arguments ###

    # #Parse arguments from command line
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-c', '--corpora_directory')
    # parser.add_argument('-v', '--vector_words_file')
    # args = parser.parse_args()
    # corporaDir = args.corpora_directory
    # vectorWordsFile = args.vector_words_file

    corporaDir = "/Users/robdow/Desktop/honors research/Coding/data/corpora/DWF_50_corpora_clean"
    vectorWordsFile = "/Users/robdow/Desktop/honors research/Coding/data/vector_words_5200_corpora.txt"

    start_time = time.time()

    main(corporaDir, vectorWordsFile)