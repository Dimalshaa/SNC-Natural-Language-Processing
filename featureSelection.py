# Feature selection, also called variable selection is a data reduction technique for selecting
# the most relevant features of a learning models. As irrelevant and redundant features are

import os
import re
import time
import numpy

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer


def prestejStavke(datoteka):
    stStavkov = 0
    stavki = datoteka.split(".")
    stStavkov = stStavkov + len(stavki) -1
    stavki = datoteka.split("!")
    stStavkov = stStavkov + len(stavki) -1
    stavki = datoteka.split("?")
    stStavkov = stStavkov + len(stavki) -1
    #print(stStavkov)
    if(stStavkov == 0): # ker ne zazna ...
        return 1
    else:
        return stStavkov

def prestejBesede(datoteka):
   # print(len(datoteka.split()))
    return len(datoteka.split())

def prestejZnake(datoteka):
    dolzinaDatoteke = len(datoteka)
    samoCrke = re.sub('[^0-9a-zA-Z]+', '', datoteka)
    #print("Samo crke: " + samoCrke)
    stZnakov = dolzinaDatoteke - len(samoCrke)
    #print("Stevilo znakov: {0}".format(stZnakov))
    return stZnakov

def prestejCrke(datoteka):
    samoCrke = re.sub('[^0-9a-zA-Z]+', '', datoteka)
    #print("Stevilo crk: {0}".format(len(samoCrke)))
    return len(samoCrke)

def splosnaStatistika(path):
    files = []
    statistika = []
    if isinstance(path, (list,)):
        for j in range(0, len(path)):
            files.extend(buildFileList(path[j]))
            for i in range(0, len(files)):
                filename = path[j] + '/' + files[i]
                content = readFile(filename)
                statistika.append("{0}|{1}|{2}|{3}|{4}|".format(files[i], prestejBesede(content), prestejZnake(content),  prestejCrke(content),  prestejStavke(content)))
            files = []
    else:
        files.extend(buildFileList(path))
        for i in range(0, len(files)):
            filename = path + '/' + files[i]
            content = readFile(filename)
            statistika.append("{0}|{1}|{2}|{3}|{4}|".format(files[i], prestejBesede(content), prestejZnake(content),prestejCrke(content), prestejStavke(content)))
    return statistika

def bagOfWords(corpus):
    vectorizer = CountVectorizer()
    print(vectorizer.fit_transform(corpus).todense())
    print(vectorizer.vocabulary_)


def LSA(corpus):
    vectorizer = TfidfVectorizer(max_df=1.0, max_features=10000, min_df=0.1, use_idf=True)
    tfidf = vectorizer.fit_transform(corpus)
    print(vectorizer.vocabulary_)
    feat_names = vectorizer.get_feature_names()
    print(feat_names)
    svd = TruncatedSVD(10)
    lsa = make_pipeline(svd, Normalizer(copy=False))
    train_lsa = lsa.fit_transform(tfidf)
    print(train_lsa)

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
   # bagOfWords(corpus)
    LSA(corpus)

    print("------STATISTIKA-------")
    statistika = splosnaStatistika('./suicide-notes-database/completers')
    for i in range(0, len(statistika)):
        print(statistika[i])