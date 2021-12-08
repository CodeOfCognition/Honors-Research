import argparse
import pandas as pd
import json
from pathlib import Path
import time
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

def loadVectorDiscourses(vectorDiscourseFile):
    with open(vectorDiscourseFile, "rt") as f:
        fin = f.read()
        vectorDiscourses = fin.split()
        f.close
    return vectorDiscourses

def createDFVector(vectorDiscourses, dataframe):
    zeros = [0]*len(vectorDiscourses)
    d = dict(zip(vectorDiscourses, zeros))
    for index, row in dataframe.iterrows():
        key = dataframe['subreddit'][index]
        d[str(key)] += 1
    return list(d.values())

def runFile(corpusDir, vectorDiscourses):
    dataframe = pd.read_csv(corpusDir, header=None)
    dataframe.columns = ["time", "subreddit", "wc", "comment"]
    return createDFVector(vectorDiscourses, dataframe)

def writeToFile(corporaDir, jsonData):
    # Gets name of corpus directory (cuts off path leading up to it)
    index = corporaDir.rfind("/")
    corporaDirName = corporaDir[index + 1:]

    outFile = os.path.join(parentdir, "data", f"discourseFrequencies_{corporaDirName}.json")
    with open(outFile, "wt") as f:
        json.dump(jsonData, f)
        f.close()

def main(corporaDir, vectorDiscourseFile):
    
    i=1
    jsonData = dict()
    vectorDiscourses = loadVectorDiscourses(vectorDiscourseFile)
    for filename in os.listdir(corporaDir):
        if filename.endswith(".csv"):
            if (i%10 == 0):
                print("--- %s seconds ---" % (time.time() - start_time))
            if (i%10 == 0):
                print("running file " + str(i) + ": " + filename)
            jsonData[filename] = runFile(f"{corporaDir}/{filename}", vectorDiscourses)
            i += 1
    writeToFile(corporaDir, jsonData)

    print(f"createDiscourseFrequencies.py finished running in {round((time.time() - start_time), 2)} seconds.")

if __name__ == "__main__":
    
    start_time = time.time()
    print("Running script: createDiscourseFrequencies.py")

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