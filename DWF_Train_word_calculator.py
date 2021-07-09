import os
import re
from nltk.probability import FreqDist
import time
import pandas as pd
import numpy as np

start_time = time.time()


def run(corpus):
    with open(corpus, "rt") as f:
        fin = f.read()

        entry_pat = "\*--\s(.*?)--\*" # Separates entries
        time_pat = '\d\d\d\d\d\d\d\d\d\d' # 10 digit pattern in first line
        subreddit_pat = '\d\d\d\d\d\d\d\d\d\d\s(.*?)\s' # what comes after 10 digit pattern in first line
        comment_pat = '\n(.*)' # what comes after the first line
        
        entries = re.findall(entry_pat, fin, re.DOTALL)

        subreddits = list()
        comments = list()
        commentWC = list()

        numEntries = len(entries)
        j = 0
        for i in range(numEntries):
            try:
                subreddit = re.search(subreddit_pat, entries[i]).group(1)
                comment = re.search(comment_pat, entries[i], re.DOTALL).group(1)
            except:
                continue
            subreddits.append(subreddit)
            comments.append(comment) #tokenizer.tokenize(comment)
            j += 1
            # print("Comment length: " + str(commentWC[i]))
        f.close

    rawData = pd.DataFrame({'subreddit': subreddits,'comment': comments})
    # sortedData = rawData.sort_values(['subreddit'], ascending=(True)).reset_index()

    i = 0
    j = 0
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for index, row in rawData.iterrows():
        currentSubreddit = rawData['subreddit'][i]
        if rawData['subreddit'][i] in dvw: #not first comment of given subreddit
            for word in rawData['comment'][i].split():
                if word.lower() in dvw[rawData['subreddit'][i]]:
                    continue
                else:
                    for letter in word:
                        if letter in punc: 
                            word = word.replace(letter, "") 
                    if word not in dvw[rawData['subreddit'][i]]:
                        dvw[rawData['subreddit'][i]].append(word.lower())
            i += 1
        else: # is first comment of given subreddit
            for word in rawData['comment'][i].split():
                for letter in word:
                    if letter in punc: 
                        word = word.replace(letter, "")
                try: # works as long as it is not the first word of the subreddit (because dict has already been created)
                    if word.lower() not in dvw[rawData['subreddit'][i]]:
                        dvw[rawData['subreddit'][i]].append(word.lower())
                except: # first word in subreddit
                    dvw[rawData['subreddit'][i]] = [word.lower()] 
            i += 1





print("--- %s seconds ---" % (time.time() - start_time))


dvw = dict() #discourse vector words
corporaDirectory = '10_corpora'
i=1
for filename in os.listdir(corporaDirectory):
            if filename.endswith(".txt"):
                if (i%1 == 0):
                    print("--- %s seconds ---" % (time.time() - start_time))
                if (i%1 == 0):
                    print("running file " + str(i) + ": " + filename)
                run(('./' + str(corporaDirectory) + '/' + filename))
                i += 1

