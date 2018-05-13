# Feature selection, also called variable selection is a data reduction technique for selecting
# the most relevant features of a learning models. As irrelevant and redundant features are

import os
import time

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer


def bagOfWords(corpus):
    vectorizer = CountVectorizer()
    print(vectorizer.fit_transform(corpus).todense())
    print(vectorizer.vocabulary_)


def LSA(corpus):
    vectorizer = TfidfVectorizer(max_df=0.75, max_features=10000, min_df=1, use_idf=True)
    tfidf = vectorizer.fit_transform(corpus)

    print(tfidf.todense())
    print(vectorizer.vocabulary_)

    print("  Actual number of tfidf features: %d" % tfidf.get_shape()[1])
    svd = TruncatedSVD(93)
    lsa = make_pipeline(svd, Normalizer(copy=False))
    explained_variance = svd.explained_variance_ratio_.sum()
    print("SVD: {}%".format(int(explained_variance * 100)))
    print(corpus)

def buildCorpus(path):
    files = []
    corpus = []
    if isinstance(path, (list,)):
        for j in range(0, len(path)):
            files.extend(buildFileList(path[j]))
            for i in range(0, len(files)):
                filename = path[j] + '/' + files[i]
                corpus.append(readFile(filename))
            files = []
    else:
        files.extend(buildFileList(path))
        for i in range(0, len(files)):
            filename = path + '/' + files[i]
            corpus.append(readFile(filename))
    return corpus


def buildFileList(path):
    files = os.listdir(path)
    return files


def readFile(dat):
    with file(dat) as f:
        string = f.read()
    return string


def saveFile(path, filename, text):
    dat = path + "/" + filename
    file_out = open(dat, 'w')
    file_out.write(text)


if __name__ == "__main__":
    # corpus from .\completers and .\elicitors
    corpus = buildCorpus(['./suicide-notes-database/completers', './suicide-notes-database/elicitors'])
    bagOfWords(corpus)
    print("bow-------------")
    LSA(corpus)