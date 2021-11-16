import pandas as pd
import json
from pathlib import Path
import time
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


global viable 
viable = [0]
# Gathers stats of cleaned corpora

def runFile(corpusDir):
    dataframe = pd.read_csv(corpusDir, header=None)
    dataframe.columns = ["time", "subreddit", "wc", "comment"]
    dataframe = dataframe.sort_values('time', ascending=(True)).reset_index()
    
    df_len = len(dataframe["time"])
    dataframe = dataframe.iloc[(2*(df_len//3)):(df_len - 1)]
    df_len = len(dataframe["time"])


    totalTokens = dataframe["wc"].sum()
    if totalTokens > 100000:
        viable[0] += 1
    totalYears = (int(dataframe["time"][len(dataframe)-1]) - int(dataframe["time"][0]))/31557600
    averageCommentLength = totalTokens//len(dataframe["comment"])
    return totalTokens, averageCommentLength, totalYears

def main(corporaDir):
    data = list()
    i=1
    for filename in os.listdir(corporaDir):
        if filename.endswith(".csv"):
            if (i%50 == 0):
                print("--- %s seconds ---" % (time.time() - start_time))
            if (i%50 == 0):
                print("running file " + str(i) + ": " + filename)
            data.append(runFile(f"{corporaDir}/{filename}"))
            i += 1
    aveTotalTokens = 0
    aveCommentTokens = 0
    aveTime = 0
    for d in data:
        aveTotalTokens += d[0]
        aveCommentTokens += d[1]
        aveTime += d[2]
    aveTotalTokens = aveTotalTokens // len(data)
    aveCommentTokens = aveCommentTokens // len(data)
    aveTime = aveTime / len(data)
    print(f"average total tokens: {aveTotalTokens}\naverage comment tokens: {aveCommentTokens}\naverage time: {aveTime}\nviable corpora: {viable}")

if __name__ == "__main__":
    
    start_time = time.time()
    corporaDir = os.path.join(parentdir, "data", "corpora", "5200_corpora_clean")
    main(corporaDir)