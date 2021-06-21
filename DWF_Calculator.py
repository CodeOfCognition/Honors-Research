import re
import numpy as np
import pandas as pd
import nltk
from scipy import spatial
import os
import math
import time

start_time = time.time()

def processFile(fileName):
    with open(fileName, "rt") as f:
        fin = f.read()

        entry_pat = "\*--\s(.*?)--\*" # Separates entries
        time_pat = '\d\d\d\d\d\d\d\d\d\d' # 10 digit pattern in first line
        subreddit_pat = '\d\d\d\d\d\d\d\d\d\d\s(.*?)\s' # what comes after 10 digit pattern in first line
        comment_pat = '\n(.*)' # what comes after the first line

        entries = re.findall(entry_pat, fin, re.DOTALL)

        times = list()
        subreddits = list()
        comments = list()
        commentWC = list()

        numEntries = len(entries)
        j = 0
        for i in range(numEntries):
            try:
                time = re.search(time_pat, entries[i]).group()
                subreddit = re.search(subreddit_pat, entries[i]).group(1)
                comment = re.search(comment_pat, entries[i], re.DOTALL).group(1)
            except:
                print('Error on filename "' + fileName + '"\nEntry #' + str(i))
                print("Error entry: " + entries[i])
                continue
            times.append(time)
            subreddits.append(subreddit)
            comments.append(comment) #tokenizer.tokenize(comment)
            commentWC.append(len(comments[j].split()))
            j += 1
            # print("Comment length: " + str(commentWC[i]))
        f.close

    rawData = pd.DataFrame({'subreddit': subreddits,'time': times,'tokenCount': commentWC,'comment': comments})
    sortedData = rawData.sort_values(['subreddit', 'time'], ascending=(True, True)).reset_index()
    # sortedData.to_csv('lorem.csv')


    i = 0
    j = 0
    currentSubreddit = sortedData['subreddit'][0]
    counter = 0
    threshold = 30000
    rangeAndCount = list()
    for index, row in sortedData.iterrows():
        if (currentSubreddit == sortedData['subreddit'][j]): #same subreddit
            counter += int(sortedData['tokenCount'][j])
            j+=1
        elif (counter < threshold): #new subreddit, last subreddit was below threshold
            i=j
            currentSubreddit = sortedData['subreddit'][j]
            counter = int(sortedData['tokenCount'][j])
            j+=1
        else: #new subreddit, last subreddit was above threshold
            rangeAndCount.append([i,j,counter, currentSubreddit])
            i=j
            currentSubreddit = sortedData['subreddit'][j]
            counter = int(sortedData['tokenCount'][j])
            j+=1
    if (counter>=threshold): #handles final subreddit in sortedData
        rangeAndCount.append([i,j-1,counter, currentSubreddit])

    subredditData = list()
    for r in rangeAndCount:
        subredditData.append(sortedData['comment'][r[0]:r[1]+1].str.cat(sep=' ').split())

    with open("train_words.txt", "rt") as f:
        fin = f.read()
        train_words = fin.split()
        f.close



    for s in subredditData:
        words = s # list all words used across comments of subreddit 0
        zeros = [0]*80346 # array of zeros; 80346 is the number of train_words (words I want WF counts of)
        dictionary1 = dict(zip(train_words, zeros)) 
        dictionary2 = dict(zip(train_words, zeros)) 
        dictionary3 = dict(zip(train_words, zeros)) 
        dictionary4 = dict(zip(train_words, zeros)) 
        totalWords = 0
        count = 0
        for word in words:
            if word in dictionary1:
                totalWords += 1
        for word in words:
            if word in dictionary1:
                if count <= (totalWords/4):
                    dictionary1[word] += 1
                    count += 1
                elif count <= ((totalWords)/2):
                    dictionary2[word] += 1
                    count += 1
                elif count <= ((3*totalWords)/4):
                    dictionary3[word] += 1
                    count += 1
                else:
                    dictionary4[word] += 1
                    count += 1

        x = pd.DataFrame({'Words': dictionary1.keys(), 'Frequency1': dictionary1.values(), 'Frequency2': dictionary2.values(), 'Frequency3': dictionary3.values(), 'Frequency4': dictionary4.values()})
        f1 = list(dictionary1.values())
        f2 = list(dictionary2.values())
        f3 = list(dictionary3.values())
        f4 = list(dictionary4.values())

        vc12 = 1-spatial.distance.cosine(f1, f2)
        vc13 = 1-spatial.distance.cosine(f1, f3)
        vc14 = 1-spatial.distance.cosine(f1, f4)
        cosineValues.append([vc12,vc13,vc14])

def analyze(cosineArray):
    vc12Ave = 0
    vc13Ave = 0
    vc14Ave = 0
    vc12SD = 0
    vc13SD = 0
    vc14SD = 0
    count = 0
    for cosineValue in cosineArray:
        vc12Ave += cosineValue[0]
        vc13Ave += cosineValue[1]
        vc14Ave += cosineValue[2]
        count +=1
    if count != 0:
        vc12Ave = vc12Ave/count
        vc13Ave = vc13Ave/count
        vc14Ave = vc14Ave/count
        for cosineValue in cosineArray:
            vc12SD += abs(cosineValue[0] - vc12Ave)**2
            vc13SD += abs(cosineValue[1] - vc13Ave)**2
            vc14SD += abs(cosineValue[2] - vc14Ave)**2
        vc12SD = math.sqrt(vc12SD/count)
        vc13SD = math.sqrt(vc13SD/count)
        vc14SD = math.sqrt(vc14SD/count)
    else:
        print("Error: no values to calculate")
    print("\nAfter " + str(count) + "trials, \n 1to2: " + str(vc12Ave) + "\tSD: " + str(vc12SD)+ "\n 1to3: " + str(vc13Ave) + "\tSD: " + str(vc13SD)+ "\n 1to4: "+ str(vc14Ave) + "\tSD: " + str(vc14SD))

cosineValues = list() # [[1 to 2, 1 to 3, 1 to 4], [], [] ...]

directoryName = 'corpora_10_users'
i = 1
for filename in os.listdir(directoryName):
        if filename.endswith(".txt"):
            print ("starting file " + str(i) + ": " + filename)
            processFile('./corpora_10_users/' + filename)
            print ("finished file " + str(i) + ": " + filename)
            i += 1
analyze(cosineValues)


print("--- %s seconds ---" % (time.time() - start_time))