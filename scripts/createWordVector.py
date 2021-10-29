import re
import csv
import time
import math
import pandas as pd
import argparse
from nltk.probability import FreqDist
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)



def runFile(fileName, vectorWords):
    with open(fileName, "rt") as f:
        fin = f.read()
        f.close

    entry_pat = "\*--\s(.*?)--\*" # Separates entries
    time_pat = '\d\d\d\d\d\d\d\d\d\d' # 10 digit pattern in first line
    comment_pat = '\n(.*)' # what comes after the first line

    entries = re.findall(entry_pat, fin, re.DOTALL)

    numEntries = len(entries)
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for i in range(numEntries):
        try:
            comment = (re.search(comment_pat, entries[i], re.DOTALL).group(1))
            for letter in comment:
                if letter in punc: 
                    comment = comment.replace(letter, "") 
            for word in comment.split():

                vectorWords[word.lower()] += 1

        except:
            continue
    return vectorWords

def removeStopWords(vectorWords):
    toRemove = list()
    with open("./data/stopList.txt", "rt") as f:
        fin = f.read()
        stopList = fin.split()
    f.close
    for key in vectorWords.keys():
        if key in stopList:
            toRemove.append(key)
    for word in toRemove:
        vectorWords.pop(word)
    return vectorWords

def writeToFile(corporaDir, vectorWords):

    # Gets name of corpus directory (cuts off path leading up to it)
    index = corporaDir.rfind("/")
    corporaDirName = corporaDir[index + 1:]

    # Writes most common vectorWords to file
    with open(f"./data/vector_words_{corporaDirName}.txt", "w") as f:
        i = 1
        for pair in vectorWords:
            if i > 150000:
                break
            f.write(pair[0] + '\n')
            i += 1
        f.close()
    


def main(corporaDir):
    vectorWords = FreqDist()
    i = 1

    # Runs each file in directory which contains all corpora
    for filename in os.listdir(corporaDir):
        if filename.endswith(".txt"):
            if (i%10 == 0):
                print(f"--- {round((time.time() - start_time), 2)} seconds ---")
                print ("Running file " + str(i) + ": " + filename)
            vectorWords = runFile(f"{corporaDir}/{filename}", vectorWords)
            i += 1

    vectorWords = removeStopWords(vectorWords)
    most_common = vectorWords.most_common(150000)
    vectorWords = sorted(vectorWords.items(), key=lambda x: x[1], reverse=True)
    writeToFile(corporaDir, vectorWords)

    print(f"genVectorWords.py finished running in {round((time.time() - start_time), 2)} seconds.")

if __name__ == "__main__":

    start_time = time.time()
    print("Running script: createWordVector.py")

    #Parse arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--corpora_directory')
    args = parser.parse_args()
    corporaDir = args.corpora_directory

    # corporaDir = os.path.join(parentdir, "data", "corpora", "50_corpora_clean")

    main(corporaDir)
