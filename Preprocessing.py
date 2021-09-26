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
#                                        ~ In progress ~                                          #
# Functions:                                                                                      #
#   - genVectorWords: generates lists of n most common words across a set of raw reddit corpora   #
#   - cleanCorpora: transforms raw corpora into csv files with stops and punctuation removed      #
#   - runGDWFCorporaGenerator: Uses IDWF_5200_corpora_discourses.txt (list of discourses used in  #
#       IDWF analysis) to build GDWF_discourses_5200 which contains all language produced across  #
#       5200 users in the aforementioned discourses. Note: IDWF_5200_corpora_discourses.txt is no #
#       longer used in IDWF analysis, but it contains the correct info for 5200 users.            #
#   - runGDWFCorporaCleaner: Creates a corpus on equal length and time of ID-W-WF_5200 corpora,   #
#     but containing randomly sampled info from all users from that time period at that time      #
#   - runLongIUWFCorporaCleaner
#   - runShortIUWFCorporaCleaner
#   - probeMinLengthAndDiscourses: finds set of all discourses used across all (5200) user        #
#     corpora. Also finds the minimum number of words in a corpus.                                #
###################################################################################################

#Possible problem: Some GDWF corpora contain only 1 person's language data


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

    def runFile(globalDiscs, fileName, corporaPath, discCSVsPath):
        
        with open(fileName, "rt") as f:
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
    for filename in os.listdir(corporaPath):
        if filename.endswith(".csv"):
            if (i%10 == 0):
                print("--- %s seconds ---" % (time.time() - start_time))
            if (i%100 == 0):
                print("running file " + str(i) + ": " + filename)
            runFile(globalDiscs, filename, corporaPath, discCSVsPath)
            
            i += 1

def runGDWFCorporaCleaner(dirPath):
  
  # Loads discourse corpus into df
    # randomly selects comments from df up to a certain number of words.
    # deletes all other rows
    # Writes new corpus as csv for further processing

    def runFile(dirPath, fileName):
        with open(dirPath + "/" + fileName, "rt") as f:
            dfData = pd.read_csv(f, header=None)
            dfData.columns = ["times", "comments"]
        f.close()


        # dfData = pd.DataFrame({'times': [1,2,3], 'comments': ["one here", "double time", "triple nipple"]})

        l = len(dfData['comments'])
        indices = np.arange(0, l).tolist()
        wordCount = 0
        value = -1
        while wordCount < 100000:
            value = random.choice(indices)
            indices.remove(value)
            wordCount += len(dfData['comments'][value].split(' '))
            if "" in dfData['comments'][value].split(' '): wordCount += -1
        #corrects last entry that may have gone over 100000
        if wordCount > 100000:
            commentList = dfData['comments'][value].split(' ')
            numToAdd = 100000 - (wordCount - (len(commentList) -1))
            newComment = ' '.join(commentList[0:numToAdd]) + " "
            dfData.at[value, 'comments'] = newComment
        newDF = dfData.drop(indices, axis=0)
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

def runLongIUWFCorporaCleaner(prePath, corporaDir):
    def runFile(corpusDir, corpus):
        dfData = pd.read_csv(corpusDir + corpus, header=None)
        dfData.columns = ["time", "subreddit", "wc", "comment"]
        dfData = (dfData.sample(frac=1)).reset_index()
        minTime = 2631739301 # initialized max value of unix time in the year 2053
        maxTime = -1
        numWords = 0 # word counter for each quantile

        q = 0 # index of current quantile 
        for index, row in dfData.iterrows():
            numWords += dfData['wc'][index]
            if numWords < 100000:
                if (dfData['time'][index] > maxTime):
                    maxTime = dfData['time'][index]
                if (dfData['time'][index] < minTime):
                    minTime = dfData['time'][index]
            else:
                if maxTime-minTime > 31536000*8:
                    #copy these dataframe rows to a new df, sort by time, print to csv
                    # print(dfData.head())
                    dfNew = dfData.loc[0:index, ['comment', 'time']]
                    # print(dfNew.head())
                    dfNew.sort_values('time', ascending=(True)).reset_index()

                    data = ""
                    for index, row in dfNew.iterrows():
                        data += dfNew['comment'][index]
                    with open("/volumes/Robbie_External_Hard_Drive/longIUWF/" + corpus[0:-4] + ".txt", "wt") as f:
                        f.write(str(maxTime-minTime) + "\n" + data)
                break

        #now we know what the smallest time is. We should check if it's smaller than a year, add it to a new file and at the top of the files say how big it is.

    

    i = 1
    for filename in os.listdir(prePath + corporaDir):
            if filename.endswith(".csv"):
                if (i%10 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                if (i%10 == 0):
                    print("running file " + str(i) + ": " + filename)
                runFile((prePath + corporaDir + '/'), filename)
                i += 1
    print("--- %s seconds ---" % (time.time() - start_time))

def runShortIUWFCorporaCleaner(prePath, corporaDir):
    def runFile(corpusDir, corpus):
        dfData = pd.read_csv(corpusDir + corpus, header=None)
        dfData.columns = ["time", "subreddit", "wc", "comment"]
        dfData = dfData.sort_values('time', ascending=(True)).reset_index()
        numWords = 0 # word counter for each quantile
        start = 0 # index of first row in quantile
        data = [""] # word data for each quantile
        times = list() # list of time ranges of each quantile
        q = 0 # index of current quantile 
        for index, row in dfData.iterrows():
            if numWords < 25000:
                data[q] += dfData['comment'][index]
                numWords += dfData['wc'][index]
            else:
                data.append("")
                times.append(dfData['time'][index-1] - dfData['time'][start])
                start = index
                numWords = 0
                q += 1
        q -= 1 # adjusted to indicate the total number quantiles created
        smallest = [0,1,2,3]
        
        for i in range(1, (q+1)-3): #range goes 1 more than number of quantiles minus (# of quantiles per 100,000 words - 1)
            if times[i] + times[i+1] + times[i+2] + times[i+3] < times[smallest[0]] + times[smallest[1]] + times[smallest[2]] + times[smallest[3]]:
                smallest = [i, i+1, i+2, i+3]
        if times[smallest[0]] + times[smallest[1]] + times[smallest[2]] + times[smallest[3]] <= 31536000/2:
            with open("/volumes/Robbie_External_Hard_Drive/shortIUWF/" + corpus[0:-4] + ".txt", "wt") as f:
                f.write(str(times[smallest[0]] + times[smallest[1]] + times[smallest[2]] + times[smallest[3]]) + "\n")
                f.write(data[smallest[0]] + data[smallest[1]] + data[smallest[2]] + data[smallest[3]])
        #now we know what the smallest time is. We should check if it's smaller than a year, add it to a new file and at the top of the files say how big it is.

    

    i = 1
    for filename in os.listdir(prePath + corporaDir):
            if filename.endswith(".csv"):
                if (i%10 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                if (i%10 == 0):
                    print("running file " + str(i) + ": " + filename)
                runFile((prePath + corporaDir + '/'), filename)
                i += 1
    print("--- %s seconds ---" % (time.time() - start_time))

#v2 is the version that accounts for 50% or less of words coming from a single corpus
count = 0
def runShortIUWFCorporaCleanerv2(prePath, corporaDir):
    def runFile(corpusDir, corpus):
        dfData = pd.read_csv(corpusDir + corpus, header=None)
        dfData.columns = ["time", "subreddit", "wc", "comment"]
        dfData = dfData.sort_values('time', ascending=(True)).reset_index()
        numWords = 0 # word counter for each quantile
        start = 0 # index of first row in quantile
        data = [""] # word data for each quantile
        contentDict = [dict()] # keeps track of subreddit/wc pairs for each quantile
        times = list() # list of time ranges of each quantile
        q = 0 # index of current quantile 


        for index, row in dfData.iterrows():
            if numWords < 25000:
                data[q] += dfData['comment'][index]
                numWords += dfData['wc'][index]
                try: # works if not the occurrence from a given subreddit
                    currentWC = contentDict[q][dfData['subreddit'][index]] # current wc of current entry's subreddit value pair in contentDir
                    contentDict[q].update({dfData['subreddit'][index]: currentWC + dfData['wc'][index]}) # updates aforementioned value pair
                except: # for the first occurrence of a given subreddit
                    contentDict[q][dfData['subreddit'][index]] = dfData['wc'][index]
            else:
                data.append("") #create new quantile with no data in it
                contentDict.append(dict()) #creates new quantile with empty dict in it
                times.append(dfData['time'][index-1] - dfData['time'][start])
                start = index
                numWords = 0
                q += 1
        q -= 1 # adjusted to indicate the total number quantiles created
        smallest = [0,1,2,3]
        
        for i in range(1, (q+1)-3): #range goes 1 more than number of quantiles minus (# of quantiles per 100,000 words - 1)
            if times[i] + times[i+1] + times[i+2] + times[i+3] < 31536000/2:
                for k, v in contentDict[i+1].items():
                    try:
                        currentWC = contentDict[i][k]
                        d = contentDict[i].update({k: v + currentWC})
                    except:
                        contentDict[i][k] = v
                for k, v in contentDict[i+2].items():
                    try:
                        currentWC = contentDict[i][k]
                        d = contentDict[i].update({k: v + currentWC})
                    except:
                        contentDict[i][k] = v
                for k, v in contentDict[i+3].items():
                    try:
                        currentWC = contentDict[i][k]
                        d = contentDict[i].update({k: v + currentWC})
                    except:
                        contentDict[i][k] = v
                max = -1
                for v in contentDict[i].values():
                    if v>max:
                        max = v
                if max < 50000:
                    print(contentDict[i])
                    global count
                    count += 1
                    break


        # if times[smallest[0]] + times[smallest[1]] + times[smallest[2]] + times[smallest[3]] <= 31536000/2:
        #     with open("/volumes/Robbie_External_Hard_Drive/shortIUWF/" + corpus[0:-4] + ".txt", "wt") as f:
        #         f.write(str(times[smallest[0]] + times[smallest[1]] + times[smallest[2]] + times[smallest[3]]) + "\n")
        #         f.write(data[smallest[0]] + data[smallest[1]] + data[smallest[2]] + data[smallest[3]])
        #now we know what the smallest time is. We should check if it's smaller than a year, add it to a new file and at the top of the files say how big it is.

    

    i = 1
    for filename in os.listdir(prePath + corporaDir):
            if filename.endswith(".csv"):
                if (i%5 == 0):
                    print("count: " + str(count))
                    print("--- %s seconds ---" % (time.time() - start_time))
                if (i%5 == 0):
                    print("running file " + str(i) + ": " + filename)
                runFile((prePath + corporaDir + '/'), filename)
                i += 1
    print("count: " + str(count))
    print("--- %s seconds ---" % (time.time() - start_time))

def runLongIUWFCorporaCleaner(prePath, corporaDir):
    def runFile(corpusDir, corpus):
        dfData = pd.read_csv(corpusDir + corpus, header=None)
        dfData.columns = ["time", "subreddit", "wc", "comment"]
        dfData = (dfData.sample(frac=1)).reset_index()
        minTime = 2631739301 # initialized max value of unix time in the year 2053
        maxTime = -1
        numWords = 0 # word counter for each quantile

        q = 0 # index of current quantile 
        for index, row in dfData.iterrows():
            numWords += dfData['wc'][index]
            if numWords < 100000:
                if (dfData['time'][index] > maxTime):
                    maxTime = dfData['time'][index]
                if (dfData['time'][index] < minTime):
                    minTime = dfData['time'][index]
            else:
                if maxTime-minTime > 31536000*8:
                    #copy these dataframe rows to a new df, sort by time, print to csv
                    # print(dfData.head())
                    dfNew = dfData.loc[0:index, ['comment', 'time']]
                    # print(dfNew.head())
                    dfNew = dfNew.sort_values('time', ascending=(True)).reset_index()

                    data = ""
                    for index, row in dfNew.iterrows():
                        data += dfNew['comment'][index]
                    with open("/volumes/Robbie_External_Hard_Drive/longIUWF/" + corpus[0:-4] + ".txt", "wt") as f:
                        f.write(str(maxTime-minTime) + "\n" + data)
                break

        #now we know what the smallest time is. We should check if it's smaller than a year, add it to a new file and at the top of the files say how big it is.

    

    i = 1
    for filename in os.listdir(prePath + corporaDir):
            if filename.endswith(".csv"):
                if (i%10 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                if (i%10 == 0):
                    print("running file " + str(i) + ": " + filename)
                runFile((prePath + corporaDir + '/'), filename)
                i += 1
    print("--- %s seconds ---" % (time.time() - start_time))

min = 999999999999
def probeMinLengthAndDiscourses(prePath, corporaDir):
    subreddits = set()
    def runFile(corpusDir, corpus):
        dfData = pd.read_csv(corpusDir + corpus, header=None)
        dfData.columns = ["time", "subreddit", "wc", "comment"]
        total = 0

        for index, row in dfData.iterrows():
            subreddits.add(dfData['subreddit'][index])
            total += dfData['wc'][index]
        global min    
        if total < min:
            min = total
    
    i = 1
    for filename in os.listdir(prePath + corporaDir):
            if filename.endswith(".csv"):
                if (i%10 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                if (i%10 == 0):
                    print("running file " + str(i) + ": " + filename)
                runFile((prePath + corporaDir + '/'), filename)
                i += 1
    with open("./helperFiles/discourseList.txt", "wt") as f:
        for discourse in subreddits:
            f.write(str(discourse) + "\n")
    print("Min user wordcount: " + str(min))

def createDFcsv(prePath, corporaDir):
    with open('/Volumes/Robbie_External_Hard_Drive/discourseFrequencies.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["corpus", "discourse vector"])

    def runFile(corpusDir, corpus):
        dfData = pd.read_csv(corpusDir + corpus, header=None)
        dfData.columns = ["time", "subreddit", "wc", "comment"]

        with open("./helperFiles/discourseList.txt", "rt") as f:
            fin = f.read()
            discourseWords = fin.split()
            f.close

        zeros = [0]*len(discourseWords)
        d = dict(zip(discourseWords, zeros)) 
        for index, row in dfData.iterrows():
            key = dfData['subreddit'][index]
            d[str(dfData['subreddit'][index])] += 1

        vectorOfDiscourses = ""
        for v in d.values():
            vectorOfDiscourses += str(v) + " "
        vectorOfDiscourses = vectorOfDiscourses[0:-1] #removes the extra space at the end

        with open('/Volumes/Robbie_External_Hard_Drive/discourseFrequencies.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([corpus[0:-4], vectorOfDiscourses])

    i=1
    for filename in os.listdir(prePath + corporaDir):
            if filename.endswith(".csv"):
                if (i%10 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                if (i%10 == 0):
                    print("running file " + str(i) + ": " + filename)
                runFile((prePath + corporaDir + '/'), filename)
                i += 1



def tester():
    df = pd.read_csv("/Volumes/Robbie_External_Hard_Drive/discourseFrequencies.csv")
    vector1 = df['discourse vector'][1].split(' ')[0:-1]
    vector2 = df['discourse vector'][2].split(' ')[0:-1]
    for i in range(0, len(vector1)):
        vector1[i] = int(vector1[i])
        vector2[i] = int(vector2[i])
    vc = 1-spatial.distance.cosine(vector1, vector2)
    print(df['corpus'][1])
    print(df['corpus'][2])
    print(vc)



createDFcsv("/Volumes/Robbie_External_Hard_Drive/", "5200_corpora_clean")

#probeMinLengthAndDiscourses("/Volumes/Robbie_External_Hard_Drive/", "5200_corpora_clean")

# runLongIUWFCorporaCleaner('./corpora/', '5200_corpora_clean', )

# runShortIUWFCorporaCleaner('/volumes/Robbie_External_Hard_Drive/', '5200_corpora_clean')
# runGDWFCorporaCleaner("./helperFiles/GDWF_discourses_5200")

### Generate file containing list of vector words ###
# genVectorWords("/volumes/Robbie_External_Hard_Drive/", "1200_corpora", 150000, True)
# genVectorWords("/volumes/Robbie_External_Hard_Drive/", "1200_corpora", 150000, False)

### Generate new, cleaned corpora ###
# cleanCorpora("/volumes/Robbie_External_Hard_Drive/", "1200_corpora", "vector_words_150000_derived_5200_corpora_stops.txt", True)

### Generate discourse corpora from IDWF corpora discourses
# runGDWFCorporaGenerator("./helperFiles/GDWF_discourses_5200/", "./corpora/5200_corpora_clean")

