import os
import re
from nltk.probability import FreqDist

def runFile(fileName):
    with open(fileName, "rt") as f:
        fin = f.read()

        entry_pat = "\*--\s(.*?)--\*" # Separates entries
        time_pat = '\d\d\d\d\d\d\d\d\d\d' # 10 digit pattern in first line
        comment_pat = '\n(.*)' # what comes after the first line

        entries = re.findall(entry_pat, fin, re.DOTALL)

        

        numEntries = len(entries)
        j = 0
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for i in range(numEntries):
            try:
                comment = (re.search(comment_pat, entries[i], re.DOTALL).group(1))
                for letter in comment:
                    if letter in punc: 
                        comment = comment.replace(letter, "") 
                for word in comment.split():

                    train_words[word.lower()] += 1

            except:
                print('Error on filename "' + fileName + '"\nEntry #' + str(i))
                print("Error entry: " + entries[i])
                continue
            j += 1
        f.close

train_words = FreqDist()
i = 1
for filename in os.listdir('corpora_10_users'):
        if filename.endswith(".txt"):
            print ("Running file " + str(i) + ": " + filename)
            runFile('./corpora_10_users/' + filename)
            i += 1
most_common = train_words.most_common(100000)
try:
    f = open("new_train_words.txt", "x")
except:
    f = open("new_train_words.txt", "w")
for pair in most_common:
    f.write(pair[0] + '\n')


#Consider removing stop words