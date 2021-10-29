import os 
import random
import time 
from scipy import spatial

start_time = time.time()


# For personal use


corporaDir = os.getcwd() + "/data/corpora/DWF_50_corpora_clean"
vectorWordsFile = "/Users/robdow/Desktop/honors research/Coding/data/vector_words_5200_corpora.txt"

# # Gets name of corpus directory (cuts off path leading up to it)
# index = corporaDir.rfind("_")
# corporaDirName = corporaDir[index + 1:]

def createQuantiles(listedDataSampled):
    check = 0
    totalWords = len(listedDataSampled)

    zeros = [0]*150000 # size of WF vector
    dictionary1 = dict(zip(vectorWords, zeros)) 
    dictionary2 = dict(zip(vectorWords, zeros)) 
    dictionary3 = dict(zip(vectorWords, zeros)) 
    dictionary4 = dict(zip(vectorWords, zeros)) 

    for i in range(totalWords):
        if i <= (totalWords//4):
            dictionary1[listedDataSampled[i]] += 1
            check += 1
        elif i <= ((totalWords)//2):
            dictionary2[listedDataSampled[i]] += 1
            check += 1
        elif i <= ((3*totalWords)//4):
            dictionary3[listedDataSampled[i]] += 1
            check += 1
        else:
            dictionary4[listedDataSampled[i]] += 1
            check += 1
    else:
        return dictionary1, dictionary2, dictionary3, dictionary4

def processQuantiles(corpus, dictionary1, dictionary2, dictionary3, dictionary4):
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
    if vc12 > .97 and vc13 > .97 and vc14 > .97 and vc23 > .97 and vc24 > .97 and vc34 > .97:
        return corpus 
    else: 
        return "-1"

def runFile(corpus, toRemove):
    with open(corpus, "rt") as f:
        fin = f.read()
        f.close()
    listedData = fin.split()

    results = createQuantiles(listedData)
    d1, d2, d3, d4 = results[0], results[1], results[2], results[3]
    badFile = processQuantiles(corpus, d1, d2, d3, d4)
    if not "-1" == badFile:
        nineseven.append(badFile)
    return toRemove

with open(vectorWordsFile, "rt") as f:
    fin = f.read()
    vectorWords = fin.split()
    f.close

nineseven = list()
toRemove = list()
i=1
for filename in os.listdir(corporaDir):
    if filename.endswith(".txt"):
        if (i%10 == 0):
            print(f"--- {round((time.time() - start_time), 2)} seconds ---")
        if (i%10 == 0):
            print(f"running file {i}: {filename}")
        toRemove = runFile(f"{corporaDir}/{filename}", toRemove)
        i += 1

for file in toRemove:
    os.remove(file)
print("Above threshold of .97:")
for file in nineseven:
    print(file)

# Did not remove the following files:
# /Users/robdow/Desktop/honors research/Coding/data/corpora/DWF_5200_corpora_clean/BlackPeopleTwitter_DubTeeDub.txt
# /Users/robdow/Desktop/honors research/Coding/data/corpora/DWF_5200_corpora_clean/NoStupidQuestions_PM_ME_UR_SCOOTER.txt
# /Users/robdow/Desktop/honors research/Coding/data/corpora/DWF_5200_corpora_clean/boardgames_uhhhclem.txt
# /Users/robdow/Desktop/honors research/Coding/data/corpora/DWF_5200_corpora_clean/podemos_Hetaroi.txt
# /Users/robdow/Desktop/honors research/Coding/data/corpora/DWF_5200_corpora_clean/TumblrInAction_GnuMag.txt
# /Users/robdow/Desktop/honors research/Coding/data/corpora/DWF_5200_corpora_clean/exzj_EinDenker.txt
# /Users/robdow/Desktop/honors research/Coding/data/corpora/DWF_5200_corpora_clean/childfree_tparkelaine.txt
# /Users/robdow/Desktop/honors research/Coding/data/corpora/DWF_5200_corpora_clean/RepublicaArgentina_GalacticLinx.txt
# /Users/robdow/Desktop/honors research/Coding/data/corpora/DWF_5200_corpora_clean/relationship_advice_sangetencre.txt
# /Users/robdow/Desktop/honors research/Coding/data/corpora/DWF_5200_corpora_clean/relationships_baffled_soap.txt
