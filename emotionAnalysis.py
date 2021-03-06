#These scores are designed to indicate comprehension difficulty. They include 
# an ease of reading and text-grade level calculation.

import os
import fnmatch
import codecs
import operator
from itertools import groupby
import emotion
from wnaffect import WNAffect
from partsOfSpeech import downloadLexicons
from partsOfSpeech import PartsOfSpeechTagger


not_punctuation = lambda w: not (len(w)==1 and (not w.isalpha()))
new_list = []

def popraviBesedilo(besedilo):
    izhod = ""
    
    for char in besedilo:
        if char.isalpha():
            if char.isupper():
                izhod+=char.lower()
            else:    
                izhod+=char
        elif char.isspace():
            izhod+=char
        elif char=="'":
            izhod+=char
        
    return izhod

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def read_file(file):
    with codecs.open(file, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read().replace('\n', '')

def getEmotions(text):
    wna = WNAffect('wordnet-1.6/', 'wn-domains-3.2/')
    pos= PartsOfSpeechTagger('./foo.null')
    
    tags=pos.partsOfSpeechTagging(text)
    #for word in filter(not_punctuation,text.split()):
    #    print word
    for tag in tags:
        if(not_punctuation(tag[0])):
            emo=wna.get_emotion(tag[0].decode('utf-8').lower(),tag[1])
            if(emo != None):
                yield tag[0],emo.name,emo.level

def getGrouped(emos, num_words):
    global new_list
    for key,group in groupby(sorted(emos,key=lambda y: y[1].decode('utf-8')) ,lambda x: x[1].decode('utf-8')):

        total=0
        count=0
        for k in group:
            total=total+k[2]
            count=count+1
        #yield key, float(total)/float(count)
        new_list.append(key)
        yield key, float(total)/float(num_words)

def getEmotionsForCorpus(root, pattern):
    downloadLexicons()
    global new_list
    files=find_files(root, pattern)

    for file in files:
        del new_list[:]
        emos=getEmotions(read_file(file))
        fixed_text = popraviBesedilo(read_file(file))
        num_words = fixed_text.count(' ')
        #yield file, getGrouped(emos, num_words)        
        yield file, getGrouped(emos, num_words), new_list


"""
for result in getEmotionsForCorpus('.','*.txt'):
    print result[0]
    for emo in result[1]:
        print emo[0]
        print emo[1]
    print '..................................'
"""

#downloadLexicons()

#files=find_files('.', '*.txt')
#for file in files:
#    emotion(read_file(file))

#wna = WNAffect('wordnet-1.6/', 'wn-domains-3.2/')


#emo = wna.get_emotion('lessons', 'NNS')

#print (emo)