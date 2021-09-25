import os
import numpy as np
import pandas as pd
from scipy import spatial
import math
import os
import time
import matplotlib.pyplot as plt
import random
import csv

start_time = time.time()

# in this file, df refers to discourse frequency

#Pretty much implemented. Just need to debug and write to file. Sept 25 7pm

dfDataFrame = pd.read_csv("/Volumes/Robbie_External_Hard_Drive/discourseFrequencies.csv") #dfDataFrame = discourse frequency data frame
l = len(dfDataFrame['corpus'])

def runFile(corpusDir, corpus):
    

    for row, index in dfDataFrame.iterrows():
        tmp = -1
        while (tmp == -1) or (tmp == index):
            tmp = random.randint(0, l-1)

        # Calculate discourse frequencies
        vector1 = dfDataFrame['discourse vector'][index].split(' ')
        vector2 = dfDataFrame['discourse vector'][tmp].split(' ')
        for i in range(0, len(vector1)):
            vector1[i] = int(vector1[i])
            vector2[i] = int(vector2[i])
        dfVC = 1-spatial.distance.cosine(vector1, vector2) #discourse frequency vector cosine

        #Calculate word frequencies
        user1 = dfDataFrame['corpus'][index]
        user2 = dfDataFrame['corpus'][tmp]

        wfDataFrame1 = pd.read_csv("/Volumes/Robbie_External_Hard_Drive/5200_corpora_clean/" + user1 + ".csv", header=None)
        wfDataFrame1.columns = ["time", "subreddit", "wc", "comment"]
        wfDataFrame2 = pd.read_csv("/Volumes/Robbie_External_Hard_Drive/5200_corpora_clean/" + user2 + ".csv", header=None)
        wfDataFrame2.columns = ["time", "subreddit", "wc", "comment"]

        with open("./helperFiles/vector_words_150000_derived_5200_corpora.txt", "rt") as f:
            fin = f.read()
            train_words = fin.split()
            f.close

        zeros = [0]*150000 # size of WF vector
        dictionary1 = dict(zip(train_words, zeros))
        dictionary2 = dict(zip(train_words, zeros)) 

        wordData1 = (wfDataFrame1['comment'].str.cat(sep=' ').split())
        wordData2 = (wfDataFrame2['comment'].str.cat(sep=' ').split())
        
        for word in wordData1:
            dictionary1[word] += 1
        for word in wordData2:
            dictionary2[word] += 1
        
        x = pd.DataFrame({'vector1': dictionary1.values(), 'vector2': dictionary2.values()})
    
        wordVector1 = list(dictionary1.values())
        wordVector2 = list(dictionary2.values())

        wfVC = 1-spatial.distance.cosine(vector1, vector2) #word frequency vector cosine

    #write df and wf to a file

def run(prePath, corporaDir):
    with open("./results/wf_df.csv", "wt") as f:
        writer = csv.writer(f)
        writer.writerow(["df similarity", "wf similarity"])

    i = 1
    for filename in os.listdir(prePath + corporaDir):
        if filename.endswith(".csv"):
            if (i%10 == 0):
                print("--- %s seconds ---" % (time.time() - start_time))
            if (i%10 == 0):
                print("running file " + str(i) + ": " + filename)
            runFile((prePath + corporaDir + '/'), filename)
            i += 1

