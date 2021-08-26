import os
import re
import csv
from nltk.probability import FreqDist
import time
import pandas as pd
import numpy as np

###################################################################################################
#                               ~ Fully functional August 20, 2021. ~                             #
# Functions:                                                                                      #
#   - genVectorWords: generates lists of n most common words across a set of raw reddit corpora   #
#   - cleanCorpora: transforms raw corpora into csv files with stops and punctuation removed      #
###################################################################################################

start_time = time.time()

def genVectorWords(prePath, corporaDir, n, includeStopWords):

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
                    continue
                j += 1
        f.close

    vector_words = FreqDist()
    i = 1
    for filename in os.listdir(prePath + corporaDir):
            if filename.endswith(".txt"):
                if (i%10 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                    print ("Running file " + str(i) + ": " + filename)
                runFile(prePath + corporaDir + '/' + filename)
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
    if not includeStopWords:
        f = open("./helperFiles/vector_words_" + str(n) + "_derived_" + str(corporaDir) + ".txt", "w")
    else:
        f = open("./helperFiles/vector_words_" + str(n) + "_derived_" + str(corporaDir) + "_stops.txt", "w")
    i = 1
    for pair in sorted_vector_words:
        if i > n:
            break
        f.write(pair[0] + '\n')
        i += 1
    f.close()

    print("--- %s seconds ---" % (time.time() - start_time))

def cleanCorpora(prePath, corporaDir, vectorWordsFile, includeStopWords):
    

    def runFile(corporaDir, filename):
        with open(prePath + corporaDir + "/" + filename, "rt") as f:
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
        f.close

        with open("./helperFiles/stopList.txt", "rt") as f:
            fin = f.read()
            stopWords = set(fin.split())
        f.close 

        toDelete = list()
        cleanComments = list()
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        wcs= list()

        if includeStopWords:
            for i in range(len(rawComments)):
                cleanComments.append([])
            for i in range(len(rawComments)):
                newWord = ""
                for word in rawComments[i].split():
                    if word.lower() in vector_words:
                        newWord += word.lower() + " "
                    else:
                        for letter in word:
                                if letter in punc: 
                                    word = word.replace(letter, "") 
                        if word in vector_words:
                            newWord += word.lower() + " "
                cleanComments[i] = newWord
            for i in range(len(cleanComments)-1, 0, -1):
                if "" == cleanComments[i]:
                    del times[i]
                    del subreddits[i]
                    del cleanComments[i]
            data = zip(times, subreddits, (cleanComments))
            filePathOG = "corpora/" + corporaDir + "_clean_stops/" + filename
            size = len(filePathOG)
            filePath = filePathOG[:size - 3] + "csv"
          

            f = open(filePath, "w")
            writer = csv.writer(f)
            writer.writerows(data)

        else:
            for i in range(len(rawComments)):
                cleanComments.append([])
            for i in range(len(rawComments)):
                newWord = ""
                wc = 0
                for word in rawComments[i].split():
                    if word.lower() in vector_words:
                        newWord += word.lower() + " "
                        wc += 1
                    else:
                        if word.lower() in stopWords:
                            continue
                        for letter in word:
                                if letter in punc: 
                                    word = word.replace(letter, "") 
                        if word in vector_words:
                            newWord += word.lower() + " "
                            wc +=1
                cleanComments[i] = newWord
                wcs.append(wc)
            if len(wcs) != len(cleanComments):
                print("Something went wrong: line 184")
            for i in range(len(cleanComments)-1, 0, -1):
                if "" == cleanComments[i]:
                    del times[i]
                    del subreddits[i]
                    del cleanComments[i]
                    wcs.pop(i)
            data = zip(times, subreddits, wcs, cleanComments)
            filePathOG = "corpora/" + corporaDir + "_clean/" + filename
            size = len(filePathOG)
            filePath = filePathOG[:size - 3] + "csv"

            f = open(filePath, "w")
            writer = csv.writer(f)
            writer.writerows(data)


        # for i in range(len(cleanComments)):
        #     print("Subreddit:\t" + subreddits[i] + "\nTime:\t" + str(times[i]) + "\nComment:\n" + str(cleanComments[i]))
    if includeStopWords:
        if not os.path.isdir("./corpora/" + corporaDir + "_clean_stops"):
            os.mkdir("./corpora/" + corporaDir + "_clean_stops")
    else:
        if not os.path.isdir("./corpora/" + corporaDir + "_clean"):
            os.mkdir("./corpora/" + corporaDir + "_clean")
    
    with open("./helperFiles/" + vectorWordsFile, "rt") as f:
        fin = f.read()
        vector_words = set(fin.split())
    f.close

    i = 1 
    for filename in os.listdir(prePath + corporaDir):
            if filename.endswith(".txt"):
                if (i%10 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                    print ("Running file " + str(i) + ": " + filename)
                runFile(corporaDir, filename)
                i += 1





### Generate file containing list of vector words ###
genVectorWords("/volumes/Robbie_External_Hard_Drive/", "5200_corpora", 150000, True)
# genVectorWords("/volumes/Robbie_External_Hard_Drive/", "10_corpora", 150000, False)

### Generate new, cleaned corpora ###
# cleanCorpora("./corpora/", "5200_corpora", "vector_words_150000_derived_5200_corpora.txt", True)

#NOTE: Still need to fix else case for stops included, add .txt








# def myMethod():
#     def runFile(fileName):
#         with open(fileName, "rt") as f:
#             data = f.readlines()
#             times = list()
#             subreddits = list()
#             comments = list()

#             for line in data:
#                 lineData = line.split(',')
#                 comment = ""
#                 for i in range(len(lineData)):
#                     if i > 1:
#                         comment += lineData[i]
#                 times.append(lineData[0])
#                 subreddits.append(lineData[1])
#                 comments.append(comment)
#             punc = '''()[]{}'"\,'''
#             newComments = list()
#             for c in comments:
#                 for letter in c:
#                     if letter in punc:
#                         c = c.replace(letter, "")
#                 newComments.append(c)
#         f.close
#         with open(fileName, "w") as f:
#             data = zip(times, subreddits, comments)
#             writer = csv.writer(f)
#             writer.writerows(data)
            

#     dirName = "./corpora/10_test/"
#     i = 0
#     for filename in os.listdir(dirName):
#             if filename.endswith(".csv"):
#                 if (i%1 == 0):
#                     print("--- %s seconds ---" % (time.time() - start_time))
#                     print ("Running file " + str(i) + ": " + filename)
#                 runFile(dirName + filename)
#                 i += 1

# myMethod()
