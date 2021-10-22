#Honors-Research

General Notes:

All models are expected to be ran in the command line from "working_directory". Please make sure you have the following directory structure before running any files. 

working_directory
├── data/
    ├── corpora/
    ├── results/
├── scripts/
├── src/


Scripts:

genVectorWords.py
Input: a directory containing unprocessed reddit corpora
Output: generates 150,000 most common words across a given set of corpora

cleanCorpora.py
Input: directory containing unprocessed reddit corpora (.txt format), set of vector words
Output: a directory containing the corresponding processed corpora. Each processed or "cleaned" corpora is a csv file containing comments which now contain exclusively vector words in them. They also contain comment metadata.



Models (located in src directory):

IUWF.py
Input:
Output:
Notes: To adjust histogram domain/co-domain, you must hardcode it. The current specifications are optimized to process the set of 5200 corpora used in this study.