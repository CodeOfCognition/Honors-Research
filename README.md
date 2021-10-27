#Honors-Research

General Notes:

All models are expected to be ran in the command line from "working_directory". Please make sure you have the following directory structure before running any files. 

working_directory
├── data/
    ├── corpora/
    ├── results/
├── scripts/
├── src/

Notes about models:

General Notes:
    - Before running any models, first run the createWordVector.py and subsequently the cleanCorpora.py scripts once.
    - When running scripts/models, input arguments expect flags. For example, a file may run as "python3 fileName.py -c "path/to/corpus"". Run "python3 fileName.py -h" for information about flags and input arguments.

DWF:
Run script createDWFCorpora.py before running this model. At this point, you have the opportunity to manually remove corpora from subreddits which are country names.


Models (located in src directory):

UWF.py
Inputs: 
    - path to directory containing cleaned corpora (flag -c)
    - path to word vector file (flag -v)
    - the number of arguments to pass in (flag -n)
    - boolean indicating whether to run the control. Pass 0 for false, 1 for true (flag -control)
Outputs:
    - file containing vector cosines for each corpus processed
    - average and standard error across corpora (printed to terminal)
    - 6 histograms: each for a different quantile pair. Histograms show cosine similaritie values for all processed corpora.
Notes: 
    - Before running this model, you must have ran createWordVector.py and cleanCorpora.py
    - To adjust histogram domain/co-domain, you must hardcode it. The current specifications are optimized to process the set of 5200 corpora used in this study.

DWF.py
Input:
    - path to directory containing cleaned corpora (flag -c)
    - path to word vector file (flag -v)
Output:
    - file containing vector cosines for each corpus processed
    - average and standard error across corpora (printed to terminal)
    - 6 histograms: each for a different quantile pair. Histograms show cosine similaritie values for all processed corpora.
Notes: 
    - Before running this model, you must have ran createWordVector.py, cleanCorpora.py, and createDWFCorpora.py
    - To adjust histogram domain/co-domain, you must hardcode it. The current specifications are optimized to process the set of 5200 corpora used in this study. 

UDF.py
Input:
    - path to directory containing cleaned corpora (flag -c)
    - path to discourse vector file (flag -v)
Output:
    - file containing vector cosines for each corpus processed
    - average and standard error across corpora (printed to terminal)
    - 6 histograms: each for a different quantile pair. Histograms show cosine similaritie values for all processed corpora.
Notes: 
    - Before running this model, you must have ran cleanCorpora.py, createDiscourseVector.py
    - To adjust histogram domain/co-domain, you must hardcode it. The current specifications are optimized to process the set of 5200 corpora used in this study. 

-------------------------------

Scripts:

createWordVector.py
Input: 
    - path to directory containing unprocessed reddit corpora (flag -c)
Output: 
    - generates a text file containing the 150,000 most common words used in the input corpora

cleanCorpora.py
Input: 
    - path to directory containing unprocessed reddit corpora (.txt format)  (flag -c)
    - path to vector words file (flag -v)
Output: 
    - a directory containing the corresponding processed corpora. 
Notes:
    - Each processed or "cleaned" corpora is a csv file containing comments which now contain exclusively vector words in them. They also contain comment metadata.

createDWFCorpora.py
Input: 
    - path to directory containing cleaned reddit corpora (flag -c)
    - path to file containing vector words (flag -v)
Output: 
    - a new directory containing 100,000-word discourse corpora.
Notes: 
    - After running this script, outlier corpora (such as bots and foreign languaged subreddits) must be removed manually. See methods section of paper for more details.

