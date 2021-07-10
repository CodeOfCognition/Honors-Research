import os
import re
from nltk.probability import FreqDist
import time

start_time = time.time()

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
for filename in os.listdir('1200_corpora'):
        if filename.endswith(".txt"):
            if (i%10 == 0):
                print("--- %s seconds ---" % (time.time() - start_time))
                print ("Running file " + str(i) + ": " + filename)
            runFile('./1200_corpora/' + filename)
            i += 1
most_common = train_words.most_common(10)
print("most common are: " + str(most_common))
sorted_train_words = sorted(train_words.items(), key=lambda x: x[1], reverse=True)
try:
    f = open("sorted_train_words.txt", "x")
except:
    f = open("sorted_train_words.txt", "w")
i = 1
for pair in sorted_train_words:
    if i == 400000:
        break
    f.write(pair[0] + '\n')
    i += 1

print("--- %s seconds ---" % (time.time() - start_time))
#Consider removing stop words 