import re
import numpy as np
import pandas as pd
import nltk
from scipy import spatial
import os
import math
import time
import matplotlib.pyplot as plt

## Does IDWF processing AND creates ID-W-WD_5200 files for faster subsequent IDWF processing
# Created files also used in GDWF processing

start_time = time.time()

def runFile(corpusDir, corpus, trainWordsFile, numTrainWords, threshold):

    dfData = pd.read_csv(corpusDir + corpus, header=None)
    dfData.columns = ["time", "subreddit", "wordcount", "comment"]
    dfData = dfData.sort_values(['subreddit', 'time'], ascending=(True, True)).reset_index()

    subredditComments = list()
    wcs = list()
    
    counter = 0
    rangeStart=0
    j=0
    wc = 0
    
    currentSubreddit = dfData['subreddit'][0]
    subredditString = ""

    validRanges = list() #includes lists of ranges with word counts of 100000+
    for index, row in dfData.iterrows():
        if (currentSubreddit == dfData['subreddit'][index]): #same subreddit
            wc += int(dfData['wordcount'][index])
        elif (wc < threshold): #new subreddit, last subreddit was below threshold
            currentSubreddit = dfData['subreddit'][index]
            rangeStart=index
            wc = int(dfData['wordcount'][index])
        else: #new subreddit, last subreddit was above threshold
            currentSubreddit = dfData['subreddit'][index]
            validRanges.append([rangeStart, index-1])
            rangeStart=index
            wcs.append(wc)
            wc = int(dfData['wordcount'][index])
    if wc>threshold: #handles last comment
        wcs.append(wc)
        validRanges.append([rangeStart,len(dfData["wordcount"])-1]) # CHECK this line
    for i in range(0, len(validRanges)):
        if not dfData['subreddit'][validRanges[i][0]] == dfData['subreddit'][validRanges[i][1]]:
            raise Exception("Error: valid ranges are incorrect. See line 43.")
        #write string of comments (already organized by time) into a new file, select min and max time, write to a file
        for j in range(validRanges[i][0],validRanges[i][1]):
            subredditString += str(dfData['comment'][j])
        
        with open("./corpora/ID-W-WF_5200/" + dfData['subreddit'][validRanges[i][0]] + "_" + corpus[0:len(corpus)-4] + ".txt", "wt") as f:
            #writes "userName,subreddit,minTime,maxTime,wordCount"
            f.write(corpus[0:len(corpus)-4] + "," + dfData['subreddit'][validRanges[i][0]] + ",")
            f.write(str(dfData['time'][validRanges[i][0]]) + "," + str(dfData['time'][validRanges[i][1]]) + "," + str(wcs[i]) + "\n")
            #writes subreddit contents
            f.write(subredditString)
        f.close()

        subredditComments.append(subredditString.split(' '))
        subredditString = ""
        

    with open(trainWordsFile, "rt") as f:
        fin = f.read()
        train_words = fin.split()
        f.close


    for words in subredditComments:
        zeros = [0]*numTrainWords # array of zeros
        dictionary1 = dict(zip(train_words, zeros)) 
        dictionary2 = dict(zip(train_words, zeros)) 
        dictionary3 = dict(zip(train_words, zeros)) 
        dictionary4 = dict(zip(train_words, zeros)) 
        totalWords = len(words)
        for i in range(totalWords - 1):
            if i <= (totalWords/4):
                dictionary1[words[i]] += 1
                i += 1
            elif i <= ((totalWords)/2):
                dictionary2[words[i]] += 1
                i += 1
            elif i <= ((3*totalWords)/4):
                dictionary3[words[i]] += 1
                i += 1
            else:
                dictionary4[words[i]] += 1
                i += 1


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

def analyze(cosineArray):
    vc12Ave = 0
    vc13Ave = 0
    vc14Ave = 0
    vc23Ave = 0
    vc24Ave = 0
    vc34Ave = 0
    vc12SD = 0
    vc13SD = 0
    vc14SD = 0
    vc23SD = 0
    vc24SD = 0
    vc34SD = 0
    count = 0
    for cosineValue in cosineArray:
        vc12Ave += cosineValue[0]
        vc13Ave += cosineValue[1]
        vc14Ave += cosineValue[2]
        vc23Ave += cosineValue[3]
        vc24Ave += cosineValue[4]
        vc34Ave += cosineValue[5]
        count +=1
    if count != 0:
        vc12Ave = vc12Ave/count
        vc13Ave = vc13Ave/count
        vc14Ave = vc14Ave/count
        vc23Ave = vc23Ave/count
        vc24Ave = vc24Ave/count
        vc34Ave = vc34Ave/count
        for cosineValue in cosineArray:
            vc12SD += abs(cosineValue[0] - vc12Ave)**2
            vc13SD += abs(cosineValue[1] - vc13Ave)**2
            vc14SD += abs(cosineValue[2] - vc14Ave)**2
            vc23SD += abs(cosineValue[3] - vc23Ave)**2
            vc24SD += abs(cosineValue[4] - vc24Ave)**2
            vc34SD += abs(cosineValue[5] - vc34Ave)**2
        vc12SD = math.sqrt(vc12SD/count)
        vc13SD = math.sqrt(vc13SD/count)
        vc14SD = math.sqrt(vc14SD/count)
        vc23SD = math.sqrt(vc23SD/count)
        vc24SD = math.sqrt(vc24SD/count)
        vc34SD = math.sqrt(vc34SD/count)

        vc12SE = vc12SD/(math.sqrt(count))
        vc13SE = vc13SD/(math.sqrt(count))
        vc14SE = vc14SD/(math.sqrt(count))
        vc23SE = vc23SD/(math.sqrt(count))
        vc24SE = vc24SD/(math.sqrt(count))
        vc34SE = vc34SD/(math.sqrt(count))
    else:
        print("Error: no values to calculate")
    print("\nAfter " + str(count) + "trials, \n 1to2: " + str(vc12Ave) + "\tSD: " + str(vc12SD)+ "\tSE: " + str(vc12SE) + "\n 1to3: " + str(vc13Ave) + "\tSD: " + str(vc13SD)+ "\tSE: " + str(vc13SE) + "\n 1to4: "+ str(vc14Ave) + "\tSD: " + str(vc14SD)+ "\tSE: " + str(vc14SE) + "\n 2to3: " + str(vc23Ave) + "\tSD: " + str(vc23SD)+ "\tSE: " + str(vc23SE) + "\n 2to4: " + str(vc24Ave) + "\tSD: " + str(vc24SD)+ "\tSE: " + str(vc24SE) + "\n 3to4: " + str(vc34Ave) + "\tSD: " + str(vc34SD) + "\tSE: " + str(vc12SE))
    print(str(vc12Ave) + "\n" + str(vc12SD) + "\n" + str(vc12SE) + "\n" + str(vc13Ave) + "\n" + str(vc13SD) + "\n" + str(vc13SE) + "\n" + str(vc14Ave) + "\n" + str(vc14SD) + "\n" + str(vc14SE) + "\n" + str(vc23Ave) + "\n" + str(vc23SD) + "\n" + str(vc23SE) + "\n" + str(vc24Ave) + "\n" + str(vc24SD) + "\n" + str(vc24SE) + "\n" + str(vc34Ave) + "\n" + str(vc34SD) +  "\n" + str(vc34SE))

def genHistogram(titlename):
    vc12 = list()
    vc13 = list()
    vc14 = list()
    vc23 = list()
    vc24 = list()
    vc34 = list()
    for valueList in cosineValues: #vc12,vc13,vc14,vc23,vc24,vc34
        vc12.append(round(valueList[0], 2))
        vc13.append(round(valueList[1], 2))
        vc14.append(round(valueList[2], 2))
        vc23.append(round(valueList[3], 2))
        vc24.append(round(valueList[4], 2))
        vc34.append(round(valueList[5], 2))

    similarityDF = pd.DataFrame({'vc12': vc12,'vc13': vc13,'vc14': vc14, 'vc23': vc23,'vc24': vc24,'vc34': vc34})
    bins100 = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.00]
    length = int(len(similarityDF['vc12']))
    hist1 = similarityDF.hist(bins=bins100, column='vc12', weights=np.ones(length) / length)
    plt.xlabel("Similarity")
    plt.ylabel("Proportion")
    plt.ylim(0,.16)
    plt.xlim(.5,1)
    plt.title("Cosine similarity times 1 to 2 \n" + titlename)
    hist2 = similarityDF.hist(bins=bins100, column='vc13', weights=np.ones(length) / length)
    plt.xlabel("Similarity")
    plt.ylabel("Proportion")
    plt.ylim(0,.16)
    plt.xlim(.5,1)
    plt.title("Cosine similarity times 1 to 3 \n" + titlename)
    hist3 = similarityDF.hist(bins=bins100, column='vc14', weights=np.ones(length) / length)
    plt.xlabel("Similarity")
    plt.ylabel("Proportion")
    plt.ylim(0,.16)
    plt.xlim(.5,1)
    plt.title("Cosine similarity times 1 to 4 \n" + titlename)
    hist4 = similarityDF.hist(bins=bins100, column='vc23', weights=np.ones(length) / length)
    plt.xlabel("Similarity")
    plt.ylabel("Proportion")
    plt.ylim(0,.16)
    plt.xlim(.5,1)
    plt.title("Cosine similarity times 2 to 3 \n" + titlename)
    hist5 = similarityDF.hist(bins=bins100, column='vc24', weights=np.ones(length) / length)
    plt.xlabel("Similarity")
    plt.ylabel("Proportion")
    plt.ylim(0,.16)
    plt.xlim(.5,1)
    plt.title("Cosine similarity times 2 to 4 \n" + titlename)
    hist6 = similarityDF.hist(bins=bins100, column='vc34', weights=np.ones(length) / length)
    plt.xlabel("Similarity")
    plt.ylabel("Proportion")
    plt.ylim(0,.16)
    plt.xlim(.5,1)
    plt.title("Cosine similarity times 3 to 4 \n" + titlename)
    plt.show()



def run(corporaDirectory, trainWordsFile, numTrainWords, threshold):

    i = 1
    for filename in os.listdir(corporaDirectory):
            if filename.endswith(".csv"):
                if (i%10 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                if (i%10 == 0):
                    print("running file " + str(i) + ": " + filename)
                runFile((corporaDirectory + '/'), filename, trainWordsFile, numTrainWords, threshold)
                i += 1
    analyze(cosineValues)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("users: " + str(5200) + "\tVector Words: " + str(trainWordsFile) + "\tThreshold: " + str(threshold))
    



cosineValues = list() # [[1 to 2, 1 to 3, 1 to 4], [], [] ...]
dwfSubreddits = list()




run("./corpora/5200_corpora_clean", "./helperFiles/vector_words_150000_derived_5200_corpora.txt", 150000, 100000) #folder of corpora, vector words file, vector length, minimum threshold per subreddit
genHistogram("(DWF: 5200 users, 150000 derived, no stops, 100000 minimum)")

#People who have >98% similarity should be flagged and investigated
