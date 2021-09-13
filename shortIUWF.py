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
            # f.write(str(times[smallest[0]] + times[smallest[1]] + times[smallest[2]] + times[smallest[3]]) + "\n")
            f.write(data[smallest[0]] + data[smallest[1]] + data[smallest[2]] + data[smallest[3]])
    #now we know what the smallest time is. We should check if it's smaller than a year, add it to a new file and at the top of the files say how big it is.

 



def run(prePath, corporaDir): 

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



run('./corpora/', '10_corpora_clean')



             

    