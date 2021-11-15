from analyzeAndGraph import analyze, genHistogram
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
import csv
    
def genHistogram(valuePairs, titlename, xMin, xMax, yMin, yMax):
    bin1 = list()
    bin2 = list()
    bin3 = list()
    bin4 = list()
    bin5 = list()
    for pair in valuePairs:
        if pair[0] < 0.2:
            bin1.append(pair[1])
        elif pair[0] < 0.4:
            bin2.append(pair[1]) 
        elif pair[0] < 0.6:
            bin3.append(pair[1]) 
        elif pair[0] < 0.8:
            bin4.append(pair[1]) 
        else:
            bin5.append(pair[1])    

    

    df = pd.DataFrame({'0.0-0.2': bin1,'0.2-0.4': bin2,'0.4-0.6': bin3, '0.6-0.8': bin4,'0.8-1.0': bin5})
    bins100 = [0.2,0.4,0.6,0.8,1.0]
    length = int(len(df['0.0-0.2']))
    hist1 = df.hist(bins=bins100, column='0.0-0.2', weights=np.ones(length) / length)
    plt.xlabel("Similarity")
    plt.ylabel("Proportion")
    plt.ylim(yMin,yMax)
    plt.xlim(xMin,xMax)
    plt.title("Cosine similarity times 1 to 2 \n" + titlename)
    hist2 = df.hist(bins=bins100, column='0.2-0.4', weights=np.ones(length) / length)
    plt.xlabel("Similarity")
    plt.ylabel("Proportion")
    plt.ylim(yMin,yMax)
    plt.xlim(xMin,xMax)
    plt.title("Cosine similarity times 1 to 3 \n" + titlename)
    hist3 = df.hist(bins=bins100, column='0.4-0.6', weights=np.ones(length) / length)
    plt.xlabel("Similarity")
    plt.ylabel("Proportion")
    plt.ylim(yMin,yMax)
    plt.xlim(xMin,xMax)
    plt.title("Cosine similarity times 1 to 4 \n" + titlename)
    hist4 = df.hist(bins=bins100, column='0.6-0.8', weights=np.ones(length) / length)
    plt.xlabel("Similarity")
    plt.ylabel("Proportion")
    plt.ylim(yMin,yMax)
    plt.xlim(xMin,xMax)
    plt.title("Cosine similarity times 2 to 3 \n" + titlename)
    hist5 = df.hist(bins=bins100, column='0.8-1.0', weights=np.ones(length) / length)
    plt.xlabel("Similarity")
    plt.ylabel("Proportion")
    plt.ylim(yMin,yMax)
    plt.xlim(xMin,xMax)
    plt.title("Cosine similarity times 2 to 4 \n" + titlename)
    plt.show()
    
filename = os.path.join(parentdir, "data", "results", "wf_df_5200_corpora_clean_saved.csv")
with open(filename, "rt") as f:
    f.readline()
    data = f.readlines()
    f.close()

pairs = list()
for pair in data:
    rawPair = pair[:-1].split(",")
    pairs.append((float(rawPair[0]), float(rawPair[1])))

pairs = sorted(pairs, key=lambda x: x[0])
print(pairs[0:5])

with open('ur_file.csv','wt') as f:
    f.write('df,wf\n')
    for row in pairs:
        f.write(f"{row[0]},{row[1]}\n")