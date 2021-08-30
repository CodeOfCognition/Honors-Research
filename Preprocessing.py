import os
import re
import csv
from nltk.probability import FreqDist
import time
import math
from scipy import spatial
import pandas as pd
import numpy as np
import random

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

def runGDWFCorporaGenerator(discCSVsPath, corporaPath):

    def runFile(globalDiscs, fileList, corporaPath, discCSVsPath):
        
        with open(fileList[0], "rt") as f:
            dfData = pd.read_csv(f, header=None)
            dfData.columns = ["times", "subreddits", "wordcounts", "comments"]
        # for i in range(len(fileList)):
        #     if not i == 0:
        #         with open(fileList[i], "rt") as f:
        #             dfTemp = pd.read_csv(f, header=None)
        #             dfTemp.columns = ["times", "subreddits", "wordcounts", "comments"]
        #             dfData = dfData.append(dfTemp, ignore_index=True, verify_integrity=True)

        
        dfData = dfData.sort_values(['subreddits'], ascending=(True)).reset_index()

        i = 0
        maxIndex = len(globalDiscs) - 1
        
        currentDisc = globalDiscs[i]
        currentOpen = globalDiscs[i]
        
        f = open(discCSVsPath + "/" + globalDiscs[i] + ".csv", "a")
        for index, row in dfData.iterrows():
            s = dfData['subreddits'][index]
            if min(str(dfData['subreddits'][index]), currentDisc) == currentDisc: # if current disc is min of each
                if dfData['subreddits'][index] == currentDisc: # if it is also the current (both are the same)...
                    if currentOpen == currentDisc: # if it's open
                        f.write(str(dfData['times'][index])+","+dfData['comments'][index]+"\n") # process line
                    else: # if it's not open, but we want to process line on currentDisc
                        f.close()
                        f = open(discCSVsPath + "/" + globalDiscs[i] + ".csv", "a")
                        currentOpen = globalDiscs[i]
                        f.write(str(dfData['times'][index])+","+dfData['comments'][index]+"\n") # process line
                
                ### REPEAT STARTS HERE ### Really needs to just redo the code that just happened...

                else: # else we're onto a new subreddit
                    #increase i, check conditions again in case processing is necessary
                    if i+1 <= maxIndex:
                        i += 1
                        currentDisc = globalDiscs[i]
                    else:
                        break
                    while(min(currentDisc, str(dfData['subreddits'][index])) == currentDisc): # while currentDisc is min of both, iterate i...
                        if dfData['subreddits'][index] != currentDisc: #...if both are also different 
                            if i+1 <= maxIndex:
                                i += 1
                                currentDisc = globalDiscs[i]
                            else:
                                break
                        else: # Else process this line
                            f.close()
                            f = open(discCSVsPath + "/" + globalDiscs[i] + ".csv", "a")
                            currentOpen = globalDiscs[i]
                            f.write(str(dfData['times'][index])+","+dfData['comments'][index]+"\n") # process line
                            break
                    if i > maxIndex:
                        break
        



    with open("./helperFiles/IDWF_5200_corpora_discourses.txt", "r") as f:
        fin = f.read()
        globalDiscs = fin.split()
        globalDiscs = sorted(globalDiscs)
        f.close()
    for disc in globalDiscs:
        if not os.path.isfile(discCSVsPath + disc + ".csv"):
            with open(discCSVsPath + disc + ".csv", "wt") as f:
                f.close()
    i=1
    fileList = list()
    for filename in os.listdir(corporaPath):
        if filename.endswith(".csv"):
            if (i%10 == 0):
                print("--- %s seconds ---" % (time.time() - start_time))
            if (i%100 == 0):
                print("running file " + str(i) + ": " + filename)
            fileList.append(corporaPath + "/" + filename)
            if i > 3910:
                runFile(globalDiscs, fileList, corporaPath, discCSVsPath)
                fileList = list()
            i += 1

def runGDWFCorporaCleaner(dirPath):
    def runFile(dirPath, fileName):
        with open(dirPath + "/" + fileName, "rt") as f:
            dfData = pd.read_csv(f, header=None)
            dfData.columns = ["times", "comments"]
        f.close()

        l = len(dfData['comments'])
        indices = np.arange(0, l-1).tolist()
        wordCount = 0
        value = -1
        while wordCount < 100000:
            value = random.choice(indices)
            indices.remove(value)
            wordCount += len(dfData['comments'][value].split(' '))
            if "" in dfData['comments'][value].split(' '): wordCount += -1
        #corrects last entry that may have gone over 100000
        if wordCount > 100000:
            print("Wordcount: " + str(wordCount))
            print("OG comment (" + str(len(dfData['comments'][value].split(' '))-1) + "): " + str(dfData['comments'][value]))
            commentList = dfData['comments'][value].split(' ')
            numToAdd = 100000 - (wordCount - (len(commentList) -1))
            print("numToAdd: " + str(numToAdd))
            newComment = ' '.join(commentList[0:numToAdd]) + " "
            print("New comment (" + str(len(newComment)) + "): " + str(newComment))
            print("Current df value: " + str(dfData['comments'][value]))
            dfData.at[value, 'comments'] = newComment
            print("Current df value: " + str(dfData['comments'][value]))
        newDF = dfData.drop(indices, axis=0)
        l2 = len(dfData["comments"])
        l3 = len(newDF["comments"])
        newDF.to_csv("./corpora/GDWF_5200_clean/" + fileName, index=False)
        
        # with open("./corpora/GDWF_5200_clean/" + fileName, "wt") as f:


    i=1
    for filename in os.listdir(dirPath):
        if filename.endswith(".csv"):
            if (i%1 == 0):
                print("--- %s seconds ---" % (time.time() - start_time))
            if (i%1 == 0):
                print("running file " + str(i) + ": " + filename)
            runFile(dirPath, filename)
            i += 1


runGDWFCorporaCleaner("./helperFiles/GDWF_discourses_5200")

### Generate file containing list of vector words ###
# genVectorWords("/volumes/Robbie_External_Hard_Drive/", "1200_corpora", 150000, True)
# genVectorWords("/volumes/Robbie_External_Hard_Drive/", "1200_corpora", 150000, False)

### Generate new, cleaned corpora ###
# cleanCorpora("/volumes/Robbie_External_Hard_Drive/", "1200_corpora", "vector_words_150000_derived_5200_corpora_stops.txt", True)

### Generate discourse corpora from IDWF corpora discourses
# runGDWFCorporaGenerator("./helperFiles/GDWF_discourses_5200/", "./corpora/5200_corpora_clean")
