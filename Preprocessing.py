import os
import re
import csv
from nltk.probability import FreqDist
import time
import pandas as pd
import numpy as np

start_time = time.time()

def genVectorWords(corporaDir, n, includeStopWords):

    def runFile(fileName):
        with open(fileName, "rt") as f:
            fin = f.read()

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
                    print('Error on filename "' + fileName + '"\nEntry #' + str(i))
                    print("Error entry: " + entries[i])
                    continue
                j += 1
        f.close

    vector_words = FreqDist()
    i = 1
    for filename in os.listdir('./corpora/' + corporaDir):
            if filename.endswith(".txt"):
                if (i%10 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                    print ("Running file " + str(i) + ": " + filename)
                runFile('./corpora/' + corporaDir + '/' + filename)
                i += 1
    if not includeStopWords:
        toRemove = list()
        with open("./helperFiles/stopList.txt", "rt") as f:
            fin = f.read()
            stopList = fin.split()
        f.close
        for key in vector_words.keys():
            if key in stopList:
                toRemove.append(key)
        for word in toRemove:
            vector_words.pop(word)

    most_common = vector_words.most_common(n)
    sorted_vector_words = sorted(vector_words.items(), key=lambda x: x[1], reverse=True)
    try:
        f = open("./helperFiles/vector_words_" + str(n) + "_derived_" + str(corporaDir), "x")
    except:
        f = open("./helperFiles/vector_words_" + str(n) + "_" + str(corporaDir), "w")
    i = 1
    for pair in sorted_vector_words:
        if i > n:
            break
        f.write(pair[0] + '\n')
        i += 1

    print("--- %s seconds ---" % (time.time() - start_time))

def cleanCorpora(corporaDir, vectorWordsFile, includeStopWords):
    if not os.path.isdir("./corpora/" + corporaDir + "_clean"):
        os.mkdir("./corpora/" + corporaDir + "_clean")
    with open("./helperFiles/" + vectorWordsFile + ".txt", "rt") as f:
        fin = f.read()
        vector_words = set(fin.split())
    f.close

    def runFile(corporaDir, filename):
        with open("/volumes/Robbie_External_Hard_Drive/" + corporaDir + "/" + filename, "rt") as f:
            fin = f.read()

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
                except:
                    continue
                times.append(time)
                subreddits.append(subreddit)
                rawComments.append(rawComment) #tokenizer.tokenize(comment)
                j += 1
                # print("Comment length: " + str(commentWC[i]))
        f.close

     

        if not includeStopWords:
            with open("./helperFiles/stopList.txt", "rt") as f:
                fin = f.read()
                stopWords = set(fin.split())
            f.close 

            cleanComments = list()
            for i in range(len(rawComments)):
                cleanComments.append([])
            punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            for i in range(len(rawComments)):
                for word in rawComments[i].split():
                    if word.lower() in vector_words:
                        cleanComments[i].append(word.lower())
                    else:
                        if word.lower() in stopWords:
                            continue
                        for letter in word:
                                if letter in punc: 
                                    word = word.replace(letter, "") 
                        if word in vector_words:
                            cleanComments[i].append(word)



        else:
            cleanComments = list()
            punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            for i in range(len(rawComments)):
                for word in rawComments[i].split():
                    word = word.lower()
                    if word in vector_words:
                        cleanComments[i].append(word)
                    else:
                        for letter in word:
                                if letter in punc: 
                                    word = word.replace(letter, "") 
                        if word in vector_words:
                            cleanComments[i].append(word)

        data = zip(times, subreddits, (cleanComments))
        f = open("corpora/" + corporaDir + "_clean/" + filename + ".csv", "w")
        writer = csv.writer(f)
        writer.writerows(data)


        # for i in range(len(cleanComments)):
        #     print("Subreddit:\t" + subreddits[i] + "\nTime:\t" + str(times[i]) + "\nComment:\n" + str(cleanComments[i]))
     
    i = 1 
    for filename in os.listdir('./corpora/' + corporaDir):
            if filename.endswith(".txt"):
                if (i%1 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                    print ("Running file " + str(i) + ": " + filename)
                runFile(corporaDir, filename)
                i += 1








### Generate file containing list of vector words ###
# genVectorWords("50_corpora", 150000, True)

### Generate new, cleaned corpora ###
cleanCorpora("10_corpora", "150000_words_stops_removed", False)

#NOTE: Still need to fix else case for stops included