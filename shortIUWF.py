import os
import re
import numpy as np
import pandas as pd
from scipy import spatial
import math
import os
import json
import time
import matplotlib.pyplot as plt

# Probs only gonna do roughly 100,000 words for now, but should change


start_time = time.time()

def runFile(corpusDir, corpus):
    dfData = pd.read_csv(corpusDir + corpus, header=None)
    dfData.columns = ["time", "subreddit", "wc", "comment"]
    dfData = dfData.sort_values('time', ascending=(True)).reset_index()
    numWords = 0 # word counter for each quantile
    start = 0 # index of first row in quantile
    data = ["", "", "", "", "", "", "", "", "", "", "", ""] # word data for each quantile
    times = list() # list of time ranges of each quantile
    q = 0 # index of current quantile 
    for index, row in dfData.iterrows():
        if numWords < 100000:
            data[q] += dfData['comment'][index]
            numWords += dfData['wc'][index]
        else:
            q += 1
            numWords = 0
            times.append(dfData['time'][index-1] - dfData['time'][start])
    q -= 1
    smallest = 0
    for i in range(1, q+1):
        if times[i] < times[smallest]:
            smallest = i
    if times[smallest] <= 31536000:
        with open("/volumes/Robbie_External_Hard_Drive/shortIUWF/" + corpus + ".txt", "wt") as f:
            f.write(str(times[smallest]) + "\n")
            f.write(data[smallest])
    #now we know what the smallest time is. We should check if it's smaller than a year, add it to a new file and at the top of the files say how big it is.

 



def run(prePath, corporaDir):

    i = 1
    for filename in os.listdir(prePath + corporaDir):
            if filename.endswith(".csv"):
                if (i%1 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                if (i%1 == 0):
                    print("running file " + str(i) + ": " + filename)
                runFile((prePath + corporaDir + '/'), filename)
                i += 1
    print("--- %s seconds ---" % (time.time() - start_time))



run('./corpora/', '10_corpora_clean')



             

    