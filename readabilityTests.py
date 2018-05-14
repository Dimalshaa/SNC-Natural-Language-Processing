#These scores are designed to indicate comprehension difficulty. They include 
# an ease of reading and text-grade level calculation.

import os
import fnmatch
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import cmudict
import codecs

prondict = cmudict.dict()

numsyllables_pronlist = lambda l: len(filter(lambda s: (s.encode('utf-8', 'ignore').lower()[-1]).isdigit(), l))

def text_statistics(text):
    word_count = get_word_count(text)
    sent_count = get_sent_count(text)
    syllable_count = sum(map(lambda w: max(numsyllables(w)), word_tokenize(text)))
    return word_count, sent_count, syllable_count


def numsyllables(word):
    try:
        return list(set(map(numsyllables_pronlist, prondict[word.lower()])))
    except KeyError:
       return [0]

not_punctuation = lambda w: not (len(w)==1 and (not w.isalpha()))
get_word_count = lambda text: len(filter(not_punctuation, word_tokenize(text)))
get_sent_count = lambda text: len(sent_tokenize(text))
flesch_formula = lambda word_count, sent_count, syllable_count : 206.835 - 1.015*word_count/sent_count - 84.6*syllable_count/word_count
fk_formula = lambda word_count, sent_count, syllable_count : 0.39 * word_count / sent_count + 11.8 * syllable_count / word_count - 15.59

def flesch(text):
    word_count, sent_count, syllable_count = text_statistics(text)
    return flesch_formula(word_count, sent_count, syllable_count)
 
def flesch_kincaid(text):
    word_count, sent_count, syllable_count = text_statistics(text)
    return fk_formula(word_count, sent_count, syllable_count)

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def read_file(file):
    with codecs.open(file, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

"""
gets string root and string file_pattern and reads all files in given root directory 
and all recursive direcories that match the pattern in file_pattern
outputs a generator yielding a multidimensional array having values
(file_path:str, flesch_readability_ease_score:num[0-100], flesch_kincaid_grade_level:num[0-10])
"""
def readibility_test(root, file_pattern):
    nltk.download('punkt')
    files=find_files(root, file_pattern)
    for file in files:
        text=read_file(file)
        yield file, flesch(text), flesch_kincaid(text)





#for result in readibility_test(".","*.txt"):
#    print result[0]