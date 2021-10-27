import os
import re
import csv
import time
import math
import pandas as pd
import argparse
from nltk.probability import FreqDist

start_time = time.time()
print("Running script: createWordVector.py")

#Parse arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--corpora_directory')
args = parser.parse_args()
corporaDir = args.corpora_directory


def runFile(fileName):
    with open(fileName, "rt") as f:
        fin = f.read()
        f.close

    entry_pat = "\*--\s(.*?)--\*" # Separates entries
    time_pat = '\d\d\d\d\d\d\d\d\d\d' # 10 digit pattern in first line
    comment_pat = '\n(.*)' # what comes after the first line

    entries = re.findall(entry_pat, fin, re.DOTALL)

    numEntries = len(entries)
    j = 0
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for i in range(numEntries):
        try:
            comment = (re.search(comment_pat, entries[i], re.DOTALL).group(1))
            for letter in comment:
                if letter in punc: 
                    comment = comment.replace(letter, "") 
            for word in comment.split():

                vector_words[word.lower()] += 1

        except:
            continue
        j += 1

def removeStopWords(vector_words):
    toRemove = list()
    with open("./data/stopList.txt", "rt") as f:
        fin = f.read()
        stopList = fin.split()
    f.close
    for key in vector_words.keys():
        if key in stopList:
            toRemove.append(key)
    for word in toRemove:
        vector_words.pop(word)
    return vector_words

    
vector_words = FreqDist()
i = 1

# Runs each file in directory which contains all corpora
for filename in os.listdir(corporaDir):
    if filename.endswith(".txt"):
        if (i%10 == 0):
            print(f"--- {round((time.time() - start_time), 2)} seconds ---")
            print ("Running file " + str(i) + ": " + filename)
        runFile(corporaDir + '/' + filename)
        i += 1

vector_words = removeStopWords(vector_words)
most_common = vector_words.most_common(150000)
sorted_vector_words = sorted(vector_words.items(), key=lambda x: x[1], reverse=True)

# Gets name of corpus directory (cuts off path leading up to it)
index = corporaDir.rfind("/")
corporaDirName = corporaDir[index + 1:]

# Writes most common vector_words to file
with open(f"./data/vector_words_{corporaDirName}.txt", "w") as f:
    i = 1
    for pair in sorted_vector_words:
        if i > 150000:
            break
        f.write(pair[0] + '\n')
        i += 1
    f.close()

print(f"genVectorWords.py finished running in {round((time.time() - start_time), 2)} seconds.")