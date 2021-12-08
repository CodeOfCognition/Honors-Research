import numpy as np
import pandas as pd
from scipy import spatial
import math
import time
import argparse
import random
import matplotlib.pyplot as plt
from analyzeAndGraph import analyze, genHistogram
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

def loadVectorDiscourses(vectorDiscoursesFile):
    with open(vectorDiscoursesFile, "rt") as f:
        fin = f.read()
        vectorDiscourses = fin.split()
        f.close
    return vectorDiscourses

def loadCorpus(corpus):
    df = pd.read_csv(corpus, header=None)
    df.columns = ["time", "subreddit", "wc", "comment"]
    df = df.sort_values('time', ascending=(True)).reset_index()

    return df

def createQuantiles(vectorDiscourses, df):

    numTrainDiscourses = len(vectorDiscourses)

    zeros = [0]*numTrainDiscourses # size of WF vector
    dictionary1 = dict(zip(vectorDiscourses, zeros)) 
    dictionary2 = dict(zip(vectorDiscourses, zeros)) 
    dictionary3 = dict(zip(vectorDiscourses, zeros)) 
    dictionary4 = dict(zip(vectorDiscourses, zeros)) 

    check = 0
    totalComments = len(df['subreddit'])
    
    for i in range(totalComments):
        if i <= (totalComments//4):
            dictionary1[str(df['subreddit'][i])] += 1
            check += 1
        elif i <= ((totalComments)//2):
            dictionary2[str(df['subreddit'][i])] += 1
            check += 1
        elif i <= ((3*totalComments)//4):
            dictionary3[str(df['subreddit'][i])] += 1
            check += 1
        else:
            dictionary4[str(df['subreddit'][i])] += 1
            check += 1
        
    return dictionary1, dictionary2, dictionary3, dictionary4

def getDiscourseCounts(dictionary1, dictionary2, dictionary3, dictionary4):
    count1, count2, count3, count4 = set(), set(), set(), set()
    for k,v in dictionary1.items():
        if not v == 0:
            count1.add(k)
    for k,v in dictionary2.items():
        if not v == 0:
            count2.add(k)
    for k,v in dictionary3.items():
        if not v == 0:
            count3.add(k)
    for k,v in dictionary4.items():
        if not v == 0:
            count4.add(k)
    return [len(count1), len(count2), len(count3), len(count4)]
            
def processAndWriteDiscourseCounts(discourseCounts, corporaDir):
    sum1, sum2, sum3, sum4 = 0,0,0,0
    for counts in discourseCounts:
        sum1 += counts[0]
        sum2 += counts[1]
        sum3 += counts[2]
        sum4 += counts[3]
    sum1 = int(sum1/len(discourseCounts))
    sum2 = int(sum2/len(discourseCounts))
    sum3 = int(sum3/len(discourseCounts))
    sum4 = int(sum4/len(discourseCounts))
    
    index = corporaDir.rfind("/")
    corporaDirName = corporaDir[index + 1:]

    with open(os.path.join(parentdir, "data", "results", f"UDF_Average_Discourse_Counts_{corporaDirName}.csv"), "wt") as f:
        f.write("quantile1, quantile2, quantile3, quantile4\n")
        f.write(f"{sum1},{sum2},{sum3},{sum4}")
        f.close()

def processQuantiles(dictionary1, dictionary2, dictionary3, dictionary4):
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
    return [vc12,vc13,vc14,vc23,vc24,vc34]

def writeResults(corporaDir, cosineValues):
    index = corporaDir.rfind("/")
    corporaDirName = corporaDir[index + 1:]
    with open("./data/results/UDF_" + corporaDirName + ".csv", "wt") as f:
        f.write("vc12,vc13,vc14,vc23,vc24,vc34\n")
        for lst in cosineValues:
            for i in range(6):
                if not i == 5:
                    f.write(str(lst[i]) + ",")
                else:
                    f.write(str(lst[i]) + "\n")

def runFile(corpus, vectorDiscourses):

    df = loadCorpus(corpus)
    results = createQuantiles(vectorDiscourses, df)
    dictionary1, dictionary2, dictionary3, dictionary4 = results[0], results[1], results[2], results[3]
    discourseCounts = getDiscourseCounts(dictionary1, dictionary2, dictionary3, dictionary4)
    cosineValue = processQuantiles(dictionary1, dictionary2, dictionary3, dictionary4)
    return cosineValue, discourseCounts


def main(corporaDir, vectorDiscoursesFile):
    vectorDiscourses = loadVectorDiscourses(vectorDiscoursesFile)
    cosineValues = list()
    discourseCounts = list()
    i = 1
    for filename in os.listdir(corporaDir):
        if filename.endswith(".csv"):
            if (i%25 == 0):
                print("--- %s seconds ---" % (time.time() - start_time))
            if (i%25 == 0):
                print("running file " + str(i) + ": " + filename)
            results = runFile((corporaDir + '/' + filename), vectorDiscourses)
            cosineValue, discourseCount = results[0], results[1]
            cosineValues.append(cosineValue)
            discourseCounts.append(discourseCount)
            i += 1
    processAndWriteDiscourseCounts(discourseCounts, corporaDir)
    writeResults(corporaDir, cosineValues)
    analyze(cosineValues)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(f"UDF analysis complete after {len(cosineValues)} trials ran.\nPlease copy the results printed above of average cosine values and standard errors.\nA copy of the resulting cosine values for each trial are printed in data/results/UDF_(nameOfCorporaDirectory).csv")
    genHistogram(cosineValues, "UDF", 0, 1, 0, 0.24)


if __name__ == "__main__":
    start_time = time.time()
    print("Running model: UDF.py")

    # # Parse arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--corpora_directory') #expects cleaned corpora 
    parser.add_argument('-v', '--vector_discourses_file')
    args = parser.parse_args()
    corporaDir = args.corpora_directory
    vectorDiscoursesFile = args.vector_discourses_file

    # corporaDir = os.path.join(parentdir, "data", "corpora", "5200_corpora_clean")
    # vectorDiscoursesFile = os.path.join(parentdir, "data", "vector_discourses_5200_corpora_clean.txt")

    main(corporaDir, vectorDiscoursesFile)
