#1. Tokenization - prepares text for analysis like word checking, 
# ambiguity checking and disambiguation.
#2. Add speech tags.

import os
import lxml.etree
import nltk 
from multiprocessing import Process, Manager, Value
import math
import json
import pickle
import codecs
import uuid
import ast
#from nltk.corpus import brown

"""
outputs file contents as string
"""
def textFileParser(filename):
    data = []
    with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as text_file:
        data=text_file.read().replace('\n', '')
    return [data]

"""
outputs file contents as string
""" 
def xmlFileParser(filename, paragraph_tag_name) : 
    from lxml.etree import tostring
    from itertools import chain
    root = lxml.etree.parse(filename).getroot()
    buffer = root.findall(paragraph_tag_name)
    output = []
    for b in buffer:
        output.append(b.text.encode('utf8'))
    
    return output

"""
gets string "folder_path" and reads all files in a given directory
supports .xml and .txt files 
outputs an array of content from those files
"""
def readFiles(folder_path, paragraph_tag_name):
    filenames = os.listdir(folder_path)
    data = []

    for i in range(0, len(filenames)):
        filename, file_extension = os.path.splitext(filenames[i]) #gets file extension
        if file_extension == ".txt":
            data.append(textFileParser(folder_path + "\\" + filenames[i]))
        elif file_extension == ".xml":
            data.append(xmlFileParser(folder_path + "\\" + filenames[i], paragraph_tag_name))
        else:
            print("File ", filenames[i], " uses unsupported file format!")

    """ for i in data:
        print(len(i)) """

    return data

"""
downloads all lexicons and other files, used by nltk
"""
def downloadLexicons(): 
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('brown')

class PartsOfSpeechTagger:
    def __init__(self, results_folder_path):
        self.data_tagged = []
        self.results_folder_path = results_folder_path

    ### single thread method
    def partsOfSpeechTagging(self, data):
        for corpus in data:
            for paragraph in corpus:
                tokenized = nltk.word_tokenize(paragraph.decode('utf-8'))
                self.data_tagged.append(nltk.pos_tag(tokenized))

    ### multi thread methods
    def tagger(self, data, processID):
        print("[PartsOfSpeechTagger] Process initialized")
        for paragraph in data:
            tokenized = nltk.word_tokenize(paragraph.decode('utf-8'))
            json_string = json.dumps(nltk.pos_tag(tokenized), ensure_ascii=False) 
            filename = self.results_folder_path + str(uuid.uuid1()) +".json"
            with open(filename, 'w') as outfile:
                json.dump(json_string, outfile) 
        
        return True

    def partsOfSpeechTaggingMultiprocessed(self, data, number_of_processes):
        data_count = 0
        for corpus in data:
            for paragraph in corpus:
                data_count += 1

        data_per_process = math.ceil(data_count / float(number_of_processes))
        process_clusters = [] # array of data split into chunks, so we can divide them among multiple threads
        temp_list = []
        counter = 0

        # splits data into process_clusters
        for corpus_index in range(0, len(data)):
            for paragraph_index in range(0, len(data[corpus_index])):
                temp_list.append(data[corpus_index][paragraph_index])
                if(len(temp_list) >= data_per_process):
                    process_clusters.append(temp_list)
                    temp_list = []
        if len(temp_list) != 0:
            process_clusters.append(temp_list)

        processes = []  # processes queue
        for i in range(0, number_of_processes):   
            if(i >= len(process_clusters)):
                break
            processes.append(Process(target = self.tagger, args = (process_clusters[i], i, )))
            processes[i].start()
            
        for k in range(0, len(processes)):
            processes[k].join() 

class PartsOfSpeechReader():
    def __init__(self, pos_folder_path, statistics_folder_path):
        self.pos_folder_path = pos_folder_path
        self.statistics_folder_path = statistics_folder_path

    # get data as an array
    def readAnalyzedData(self):
        filenames = os.listdir(self.pos_folder_path)
        output = []
        for i in range(0, len(filenames)):
            with open(self.pos_folder_path + filenames[i]) as json_data_encrypted:
                note = json.load(json_data_encrypted)
                output.append(note)
        return output
 
    # save to file
    def save_obj(self, obj):
        with open(self.statistics_folder_path + str(uuid.uuid1()) + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    # save dictionaries of selected notes into a statistics files folder
    def partsOfSpeechStatistics(self, pos_data):
        notes = pos_data
        for note in notes:
            note = ast.literal_eval(note)
            dict = {}
            for tagged_word in note:
                if tagged_word[1] in dict:
                    dict[tagged_word[1]] += 1.0
                else:
                    dict[tagged_word[1]] = 1.0

            self.save_obj(dict)

            """
            for tag in dict:
                print tag, ' : ', dict[tag]
            """
        return

    # load from file
    def load_obj(self):
        filenames = os.listdir(self.statistics_folder_path)
        output = []
        for i in range(0, len(filenames)):
            with open(self.statistics_folder_path + filenames[i], 'rb') as f:
                output.append(pickle.load(f))
        return output

    # gets median values
    def getMedianStatistics(self):
        dictionaries = self.load_obj()
        results = {}
        for d in dictionaries:
            for key in d:
                if key in results:
                    results[key] += d[key]
                else:
                    results[key] = d[key]
        
        for key in results:
            #print key, " : ", results[key]
            results[key] /= len(dictionaries)
            #print key, " : ", results[key]
        
        return results



if __name__ == "__main__":
    #downloadLexicons()
    data = readFiles("./suicide-notes-database/completers/", ".//post")
    pos = PartsOfSpeechTagger("./suicide-notes-database/parts_of_speech/")

    # single threaded tagger
    #pos.partsOfSpeechTagging(data)
    #print(len(pos.data_tagged))

    # multi threaded tagger
    #pos.partsOfSpeechTaggingMultiprocessed(data, 6)

    # reader : statistics
    pos_reader = PartsOfSpeechReader(
        "./suicide-notes-database/parts_of_speech/",
        "./suicide-notes-database/parts_of_speech_statistics/"
        )
    #pos_data = pos_reader.readAnalyzedData()
    #pos_reader.partsOfSpeechStatistics(pos_data)
    statistics = pos_reader.getMedianStatistics()



