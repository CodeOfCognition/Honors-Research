import re
import csv
import time
import math
import pandas as pd
import argparse
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


def runFile(corpus, vectorDiscourses):
    df = pd.read_csv(corpus, header=None)
    df.columns = ["time", "subreddit", "wc", "comment"]
    for index, row in df.iterrows():
        vectorDiscourses.add(str(df["subreddit"][index]))
    return vectorDiscourses

def writeResults(vectorDiscourses):
    index = corporaDir.rfind("/")
    corporaDirName = corporaDir[index + 1:]
    with open(os.path.join(parentdir, "data", f"vector_discourses_{corporaDirName}.txt"), "wt") as f:
        i = 0
        for d in vectorDiscourses:
            f.write(d)
            if not i == len(vectorDiscourses) -1:
                f.write("\n")
            i += 1

def main(corporaDir): 
    vectorDiscourses = set()
    i = 1
    for filename in os.listdir(corporaDir):
        if filename.endswith(".csv"):
            if (i%10 == 0):
                print(f"--- {round((time.time() - start_time), 2)} seconds ---")
                print ("Running file " + str(i) + ": " + filename)
            vectorDiscourses = runFile(corporaDir + '/' + filename, vectorDiscourses)
            i += 1

    writeResults(vectorDiscourses)

if __name__ == "__main__":

    start_time = time.time()
    print("Running script: createDicourseVector.py")

    # Parse arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--corpora_directory') #expects cleaned corpora 
    args = parser.parse_args()
    corporaDir = args.corpora_directory

    # corporaDir = os.path.join(parentdir, "data", "corpora", "50_corpora_clean")

    main(corporaDir)


