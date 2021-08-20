import os
for filename in os.listdir("./corpora/5200_corpora_clean"):
    old = "./corpora/5200_corpora_clean/" + filename
    new = old[:len(old) - 7] + "csv"
    os.rename(old, new)