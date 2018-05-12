# Feature selection, also called variable selection is a data reduction technique for selecting
# the most relevant features of a learning models. As irrelevant and redundant features are

import os
from sklearn.feature_extraction.text import CountVectorizer


def bagOfWords(corpus):
    vectorizer = CountVectorizer()
    print(vectorizer.fit_transform(corpus).todense())
    print(vectorizer.vocabulary_)
    
def buildCorpus(path):
    files = []
    corpus = []
    if isinstance(path, (list,)):
        for j in range(0, len(path)):
            files.extend(buildFileList(path[j]))
            for i in range(0, len(files)):
                filename = path[j] + '/' + files[i]
                corpus.append(readFile(filename))
            files=[]
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
    corpus = buildCorpus(['.\suicide-notes-database\completers', '.\suicide-notes-database\elicitors'])
    bagOfWords(corpus)
