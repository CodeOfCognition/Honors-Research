import os
import re
import csv
import time
import math
import pandas as pd
import argparse

start_time = time.time()
print("Running script: cleanCorpora.py")

#Parse arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--corpora_directory')
parser.add_argument('-v', '--vector_words_file')
args = parser.parse_args()
corporaDir = args.corpora_directory
vectorWordsFile = args.vector_words_file

# Gets name of corpus directory (cuts off path leading up to it)
index = corporaDir.rfind("/")
corporaDirName = corporaDir[index + 1:]

def extractCorpusInformation(filename):
    with open(corporaDir + "/" + filename, "rt") as f:
        fin = f.read()
        f.close

        entry_pat = "\*--\s(.*?)--\*" # Separates entries
        time_pat = '\d\d\d\d\d\d\d\d\d\d' # 10 digit pattern in first line
        subreddit_pat = '\d\d\d\d\d\d\d\d\d\d\s(.*?)\s' # what comes after 10 digit pattern in first line
        comment_pat = '\n(.*)' # what comes after the first line
        
        entries = re.findall(entry_pat, fin, re.DOTALL)

        subreddits = list()
        times = list()
        rawComments = list()

        numEntries = len(entries)
        j = 0
        for i in range(numEntries):
            try:
                time = re.search(time_pat, entries[i]).group()
                subreddit = re.search(subreddit_pat, entries[i]).group(1)
                rawComment = re.search(comment_pat, entries[i], re.DOTALL).group(1)
            except: # Handles malformed entries
                continue
            times.append(time)
            subreddits.append(subreddit)
            rawComments.append(rawComment)
            j += 1
        return times, subreddits, rawComments

def cleanComments(rawComments):

    with open("./data/stopList.txt", "rt") as f:
        fin = f.read()
        f.close 
    
    stopWords = set(fin.split())
    cleanedComments = list()
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    wordCounts= list() # word counts: list of word counts for each cleaned comment

    for i in range(len(rawComments)):
        cleanedComments.append([])

    for i in range(len(rawComments)):
        newWord = ""
        wc = 0
        for word in rawComments[i].split():
            word = word.lower()
            if word in stopWords:
                continue
            elif word in vectorWords:
                newWord += word + " "
                wc += 1
            else:
                for letter in word:
                        if letter in punc: 
                            word = word.replace(letter, "") 
                if word in vectorWords:
                    newWord += word.lower() + " "
                    wc +=1
        cleanedComments[i] = newWord
        wordCounts.append(wc)
    return cleanedComments, wordCounts

def runFile(filename):
    
    corpusInfo = extractCorpusInformation(filename)
    times, subreddits, rawComments = corpusInfo[0], corpusInfo[1], corpusInfo[2]

    results = cleanComments(rawComments)
    cleanedComments, wordCounts = results[0], results[1]

    # Handles comments that contained only stop words or words not in vector space
    for i in range(len(cleanedComments)-1, 0, -1):
        if "" == cleanedComments[i]:
            del times[i]
            del subreddits[i]
            del cleanedComments[i]
            wordCounts.pop(i)

    data = zip(times, subreddits, wordCounts, cleanedComments)
    filePath = "data/corpora/" + corporaDirName + "_clean/" + filename
    size = len(filePath)
    filePath = filePath[:size - 3] + "csv"

    f = open(filePath, "w")
    writer = csv.writer(f)
    writer.writerows(data)



if not os.path.isdir("./data/corpora/" + corporaDirName + "_clean"):
    os.mkdir("./data/corpora/" + corporaDirName + "_clean")

with open(vectorWordsFile, "rt") as f:
    fin = f.read()
    f.close
vectorWords = set(fin.split())

i = 1 
for filename in os.listdir(corporaDir):
        if filename.endswith(".txt"):
            if (i%10 == 0):
                print(f"--- {round((time.time() - start_time), 2)} seconds ---")
                print ("Running file " + str(i) + ": " + filename)
            runFile(filename)
            i += 1

print(f"cleanCorpora.py finished running in {round((time.time() - start_time), 2)} seconds.")