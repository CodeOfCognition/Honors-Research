import re
import numpy as np
import pandas as pd
import nltk
from scipy import spatial
import os
import math
import time
import matplotlib.pyplot as plt

start_time = time.time()



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
        


def run(discCSVsPath, corporaPath):
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
            if (i%10 == 0):
                print("running file " + str(i) + ": " + filename)
            fileList.append(corporaPath + "/" + filename)
            if i % 1 == 0:
                runFile(globalDiscs, fileList, corporaPath, discCSVsPath)
                fileList = list()
            i += 1




run("./helperFiles/GDWF_discourses_5200/", "./corpora/5200_corpora_clean")
