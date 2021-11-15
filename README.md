#Honors-Research

## Table of Contents
1. [General Notes](#General-Notes)  
2. [Models](#Models)  
a. [DWF](#DWF.py)  
b. [UWF](#UWF.py)  
c. [UDF](#UDF.py)  
3. [Scripts](#Scripts)  
a. [createWordVector.py](#createWordVector.py)  
b. [cleanCorpora.py](#cleanCorpora.py)  
c. [createDWFCorpora.py](#createDWFCorpora.py)  
d. [createDiscourseVector.py](#createDiscourseVector.py)  
e. [createDiscourseFrequencies.py](#createDiscourseFrequencies.py)  



### General-Notes


#### Important Note Before Running Code:
- All models are expected to be ran in the command line from "working_directory". Please make sure you have the following directory structure before running any files. 
- Before running any models, first run the createWordVector.py and subsequently the cleanCorpora.py scripts once.
- When running scripts/models, input arguments expect flags. For example, a file may run as "python3 fileName.py -c data/corpora/myCorpus". Run "python3 fileName.py -h" for information about flags and input arguments.

#### Directory structure

working_directory  
├── data/  
&emsp;&emsp;├── corpora/  
&emsp;&emsp;├── results/  
├── scripts/  
├── src/  

#### Key terms:
  - **word vector**: a vector of the most 150,000 common words across a given set of corpora
  - **vector words**: the words in the word vector
  - **discourse vector**: a vector containing the set of all subreddits (discourses) used across a given set of corpora
  - **vector discourses**: the discourses (subreddits) in a discourse vector

-------------------------------

## Models

#### UWF.py
###### Inputs: directory containing cleaned corpora (flag -c)
  - word vector file (flag -v)
  - the number of arguments to pass in (flag -n)
  - boolean indicating whether to run the control. Pass 0 for false, 1 for true (flag -control)

###### Outputs:
  - file containing vector cosines for each corpus processed
  - average and standard error across corpora (printed to terminal)
  - 6 histograms: each for a different quantile pair. Histograms show cosine similaritie values for all processed corpora.

###### Notes: 
  - Before running this model, you must have ran createWordVector.py and cleanCorpora.py
  - To adjust histogram domain/co-domain, you must hardcode it. The current specifications are optimized to process the set of 5200 corpora used in this study.

#### DWF.py
###### Input:
  - directory containing cleaned corpora (flag -c)
  - word vector file (flag -v)

###### Output:
  - file containing vector cosines for each corpus processed
  - average and standard error across corpora (printed to terminal)
  - 6 histograms: each for a different quantile pair. Histograms show cosine similaritie values for all processed corpora.

###### Notes: 
  - Before running this model, you must have ran createWordVector.py, cleanCorpora.py, and createDWFCorpora.py (in that order)
  - To adjust histogram domain/co-domain, you must hardcode it. The current specifications are optimized to process the set of 5200 corpora used in this study. 

#### UDF.py
###### Input:
  - directory containing cleaned corpora (flag -c)
  - discourse vector file (flag -v)

###### Output:
  - file containing vector cosines for each corpus processed
  - average and standard error across corpora (printed to terminal)
  - 6 histograms: each for a different quantile pair. Histograms show cosine similaritie values for all processed corpora.

###### Notes: 
  - Before running this model, you must have ran cleanCorpora.py, createDiscourseVector.py
  - To adjust histogram domain/co-domain, you must hardcode it. The current specifications are optimized to process the set of 5200 corpora used in this study. 

#### WFxDF.py
###### Input:
  - directory containing cleaned corpora (flag -c)
  - word vector file (-vw)
  - integer that specifies bin size (-b) 

###### Output:
  - csv file containing 5*(bin size) discourse frequency and word frequency values taken between pairs of corpora.

###### Notes:
  - There are five bins evenly distributed over range (0,1) of discourse frequency. The bin size refers to the value of **each** of these 5 bins.


## Scripts

#### createWordVector.py
###### Input: 
  - directory containing unprocessed reddit corpora (flag -c)

###### Output: 
  - generates a text file containing the 150,000 most common words used in the input corpora

#### cleanCorpora.py
###### Input: 
  - directory containing unprocessed reddit corpora (.txt format)  (flag -c)
  - word vector file (flag -v)

###### Output: 
  - a directory containing the corresponding processed corpora. 

###### Notes:
  - Each processed or "cleaned" corpus is a csv file containing comments whose words are lower-cased, stripped of symbols, and subsequently removed if they are not present in the inputted word vector. They also contain comment metadata. Each entry consists of UNIX time, subreddit (discourse), wordcount, and then comment.

#### createDWFCorpora.py
###### Input: 
  - directory containing cleaned reddit corpora (flag -c)
  - word vector file (flag -v)

###### Output: 
  - a new directory containing 100,000-word discourse corpora.

###### Notes: 
  - After running this script, outlier corpora (such as bots and foreign languaged subreddits) must be removed manually. See methods section of paper for more details.

#### createDiscourseVector.py
###### Input:
  - directory containing cleaned reddit corpora (flag -c)

###### Output:
  - discourse vector file

#### createDiscourseFrequencies.py
###### Input:
  - directory containing cleaned reddit corpora (flag -c)
  - discourse vector file (flag -v)

###### Output:
  - json file containing a dictionary with keys that are corpus names and values that are lists of discourse frequencies. Discourse frequencies are vectors of numbers which correspond to the number of times a comment was made in a subreddit.
