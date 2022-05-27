import numpy as np


embeddings_dict = {}
word_dict = {}
with open("../model/cc.bo.300.vec", 'r', encoding="utf-8") as f:
    for idx, line in enumerate(f):
        values = line.split()
        word = values[0]
        word_dict[word] = idx
        vector = np.asarray(values[1:], "float32")
        embeddings_dict[word] = vector
np.save('../model/bo_wordsDict', np.array(word_dict))
np.save('../model/bo_wordVectors', np.array(list(embeddings_dict.values()), dtype='float32'))
