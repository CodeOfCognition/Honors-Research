import re
import numpy as np
import pandas as pd
import nltk
from scipy import spatial
import random
import os
import math
import time
import matplotlib.pyplot as plt
import argparse


def importData(corpus):
    df = pd.read_csv(corpus, header=None)
    df.columns = ["time", "subreddit", "wordcount", "comment"]
    df = df.sort_values(['subreddit', 'time'], ascending=(True, True)).reset_index()
    return df

def findUsableDiscourseRanges(df):
    wcs = list()
    rangeStart=0
    wc = 0
    threshold = 100000
    currentSubreddit = df['subreddit'][0]

    discourseTimeRanges = list() #includes lists of ranges with word counts of 100000+
    for index, row in df.iterrows():
        if (currentSubreddit == df['subreddit'][index]): #same subreddit
            wc += int(df['wordcount'][index])
        elif (wc < threshold): #new subreddit, last subreddit was below threshold
            currentSubreddit = df['subreddit'][index]
            rangeStart=index
            wc = int(df['wordcount'][index])
        else: #new subreddit, last subreddit was above threshold
            currentSubreddit = df['subreddit'][index]
            discourseTimeRanges.append(df["time"][index - 1] - df["time"][rangeStart]) # 
            rangeStart=index
            wc = int(df['wordcount'][index])
    if wc>threshold: #handles last comment
        discourseTimeRanges.append(df["time"][len(df["time"]) - 1] - df["time"][rangeStart]) # 
    return discourseTimeRanges

def runFile(corpus):

    df = importData(corpus)
    return findUsableDiscourseRanges(df)

def main(corporaDir):

    times = list() 

    i = 1
    for filename in os.listdir(corporaDir):
        if filename.endswith(".csv"):
            if (i%10 == 0):
                print(f"--- {round((time.time() - start_time), 2)} seconds ---")
            if (i%10 == 0):
                print(f"running file {i}: {filename}")
            newTimes = runFile(f"{corporaDir}/{filename}")
            if len(newTimes) > 0:
                for t in newTimes:
                    times.append(t)
            if i+1 % 40 == 0:
                average = 0
                for t in times:
                    average += t
                average = average / len(times)
                print(f"Average time: {average}")
            i += 1
    average = 0
    for t in times:
        average += t
    average = average / len(times)
    print(f"Average time: {average}")
    print(f"Number of files analyzed: {len(times)}")
    print(f"analysis finished running in {round((time.time() - start_time), 2)} seconds.")

if __name__ == "__main__":
    
    start_time = time.time()

    corporaDir = "/Users/robdow/Desktop/honors research/Coding/data/corpora/5200_corpora_clean"
    
    main(corporaDir)